import express from "express";
import fetch from "node-fetch";

const app = express();

app.get("/", (req, res) => {
  res.send("🚀 Land Checker Bot is running!");
});

const TELEGRAM_BOT_TOKEN = "ضع_رمز_بوتك_هنا";
const TELEGRAM_CHAT_ID = "1244229957"; // مثال: رقم معرفك في التليجرام

async function sendTelegramMessage(text) {
  const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;
  await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_id: TELEGRAM_CHAT_ID, text }),
  });
}

// إرسال رسالة عند تشغيل السيرفر
sendTelegramMessage("✅ البوت يعمل الآن ويراقب الأراضي.");

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server runni
