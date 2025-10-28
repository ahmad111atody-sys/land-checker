#!/usr/bin/env python3
"""
check_sakani.py
فحص روابط sakani الموجودة في ملف نصي واحد (واحد في السطر)
ينتج ملف CSV: unit_id,url,http_status,found_keywords,verdict,last_checked

متطلبات:
  pip install aiohttp aiodns cchardet beautifulsoup4 pandas

استخدام نموذجي:
  python check_sakani.py --input sahban.txt --output results.csv --workers 30 --timeout 12

خيارات مهمة:
  --prefix  : إذا تريد تضيف "/check_land" قبل كل مسار (مثلاً: /check_land/units/12345)
  --neg-kw  : كلمات عربية تفيد أن القطعة ملغاة، مفصولة بفواصل (الافتراضي جيد)
  --pos-kw  : كلمات تدل على التوفر (اختياري)
"""
import argparse
import asyncio
import aiohttp
import csv
import re
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse, urlunparse
import sys

DEFAULT_NEGATIVE_KEYWORDS = [
    "ملغاة", "ملغية", "ملغى", "ملغي", "غير متاح", "غير متوفر", "محجوز", "ملغى الطلب",
    "غير متاحة", "لم تعد متاحة", "غير متاحه"
]
DEFAULT_POSITIVE_KEYWORDS = [
    "متاح", "متوفرة", "متوفّر", "متوفر", "متاحة", "إتاحة", "متاحة الآن"
]

re_unit = re.compile(r'/units/(\d+)', re.IGNORECASE)

def extract_unit_id(url):
    m = re_unit.search(url)
    return m.group(1) if m else ""

async def fetch(session, url, timeout):
    try:
        async with session.get(url, timeout=timeout, allow_redirects=True) as resp:
            text = await resp.text(errors='ignore')
            return resp.status, text
    except asyncio.TimeoutError:
        return "timeout", ""
    except aiohttp.ClientResponseError as e:
        return e.status if hasattr(e, "status") else "http_err", ""
    except Exception as e:
        return "error", f"{type(e).__name__}: {str(e)}"

def analyze_html(html, pos_keywords, neg_keywords):
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    # get textual content (page)
    text = soup.get_text(separator=" ").lower()
    found = []
    for kw in neg_keywords:
        if kw.lower() in text:
            found.append(kw)
    for kw in pos_keywords:
        if kw.lower() in text:
            found.append(kw)
    # also check titles/meta
    title = (soup.title.string or "") if soup.title else ""
    if title:
        t = title.lower()
        for kw in neg_keywords + pos_keywords:
            if kw.lower() in t and kw not in found:
                found.append(kw)
    return list(dict.fromkeys(found))  # dedupe, preserve order

def decide_verdict(http_status, found_keywords, neg_keywords_set, pos_keywords_set):
    # priority: explicit negative keywords -> negative, explicit positive -> available
    if isinstance(http_status, int) and http_status >= 400:
        return "not_found_or_error"
    if http_status == "timeout":
        return "timeout"
    if http_status == "error":
        return "error"
    if found_keywords:
        for k in found_keywords:
            kl = k.lower()
            if kl in neg_keywords_set:
                return "cancelled"
            if kl in pos_keywords_set:
                return "available"
    # otherwise unknown/needs manual check
    return "unknown"

async def worker(name, session, queue, writer, args, neg_keywords_set, pos_keywords_set):
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        orig_url = item
        # possibly add prefix
        if args.prefix:
            # insert prefix after domain, keep leading slash correctness
            p = urlparse(orig_url)
            new_path = args.prefix.rstrip("/") + p.path if not p.path.startswith(args.prefix) else p.path
            p = p._replace(path=new_path)
            url = urlunparse(p)
        else:
            url = orig_url
        unit_id = extract_unit_id(url) or ""
        status, html = await fetch(session, url, timeout=args.timeout)
        found = analyze_html(html, args.pos_kw_list, args.neg_kw_list)
        verdict = decide_verdict(status if isinstance(status, int) else status, found,
                                 neg_keywords_set, pos_keywords_set)
        last_checked = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        # write CSV row
        writer.writerow({
            "unit_id": unit_id,
            "url": url,
            "http_status": status,
            "found_keywords": ";".join(found),
            "verdict": verdict,
            "last_checked": last_checked
        })
        # flush to disk if file-like with flush
        try:
            sys.stdout.write(f"\r[{name}] checked {unit_id or url} -> {verdict}    ")
            sys.stdout.flush()
        except Exception:
            pass
        queue.task_done()

async def main_async(args):
    # read URLs
    with open(args.input, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]
    # prepare keywords lists
    neg_kw_list = [k.strip() for k in args.neg_kw.split(",") if k.strip()] if args.neg_kw else DEFAULT_NEGATIVE_KEYWORDS
    pos_kw_list = [k.strip() for k in args.pos_kw.split(",") if k.strip()] if args.pos_kw else DEFAULT_POSITIVE_KEYWORDS
    args.neg_kw_list = neg_kw_list
    args.pos_kw_list = pos_kw_list
    neg_set = set([k.lower() for k in neg_kw_list])
    pos_set = set([k.lower() for k in pos_kw_list])

    # prepare CSV
    out_f = open(args.output, "w", newline="", encoding="utf-8")
    fieldnames = ["unit_id", "url", "http_status", "found_keywords", "verdict", "last_checked"]
    writer = csv.DictWriter(out_f, fieldnames=fieldnames)
    writer.writeheader()

    # aiohttp session
    conn = aiohttp.TCPConnector(limit_per_host=args.workers, ssl=False)
    timeout = aiohttp.ClientTimeout(total=None, sock_connect=args.timeout, sock_read=args.timeout)
    async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
        queue = asyncio.Queue()
        for u in urls:
            await queue.put(u)
        # workers
        tasks = []
        for i in range(args.workers):
            t = asyncio.create_task(worker(f"W{i+1}", session, queue, writer, args, neg_set, pos_set))
            tasks.append(t)
        # put stop signals
        await queue.join()
        for _ in range(args.workers):
            await queue.put(None)
        await asyncio.gather(*tasks)

    out_f.close()
    print("\nDone. Results saved to:", args.output)

def parse_args():
    p = argparse.ArgumentParser(description="فحص روابط Sakani من ملف وإنتاج ملف CSV بالحالة")
    p.add_argument("--input", "-i", required=True, help="ملف نصي (واحد URL في كل سطر)")
    p.add_argument("--output", "-o", default="results.csv", help="اسم ملف CSV الناتج")
    p.add_argument("--workers", "-w", type=int, default=20, help="عدد العمال المتوازيين (افتراضي 20)")
    p.add_argument("--timeout", "-t", type=int, default=12, help="Timeout لكل طلب بالثواني")
    p.add_argument("--prefix", "-p", default="", help="بادئة تضيفها لمسار URL (مثل /check_land)")
    p.add_argument("--neg-kw", dest="neg_kw", default=",".join(DEFAULT_NEGATIVE_KEYWORDS),
                   help="كلمات تدل على أن القطعة ملغاة (مفصولة بفواصل)")
    p.add_argument("--pos-kw", dest="pos_kw", default=",".join(DEFAULT_POSITIVE_KEYWORDS),
                   help="كلمات تدل على توفر القطعة (اختياري)")
    return p.parse_args()

def main():
    args = parse_args()
    try:
        asyncio.run(main_async(args))
    except KeyboardInterrupt:
        print("\nInterrupted by user")

if __name__ == "__main__":
    main()
