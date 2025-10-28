import TelegramBot from "node-telegram-bot-api";
import express from "express";
import axios from "axios";

// 🔐 بياناتك الخاصة
const token = "8497253482:AAH8z9Ib6x5K3oUllKXbejWDUNsBBu9Foco"; // توكن البوت
const CHAT_ID = "1244229957"; // معرفك في التليجرام

// ⚙️ إعداد السيرفر والبوت
const bot = new TelegramBot(token, { polling: true });
const app = express();

app.get("/", (req, res) => {
  res.send("✅ Bot is running and watching Sakani projects...");
});

// ✅ اختبار البوت
bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id, "مرحباً 👋 البوت يعمل الآن بنجاح!");
});

bot.onText(/\/ping/, (msg) => {
  bot.sendMessage(msg.chat.id, "🏓 البوت متصل ويعمل تمام ✅");
});

// 🌙 دالة الفحص
async function checkSakaniProjects() {
  try {
    const url = "https://sakani.sa/app/land-projects/146"; // رابط المخطط
    const res = await axios.get(url, {
      headers: {
        "User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        Accept: "application/json,text/html;q=0.9",
      },
    });

    console.log("Checked Sakani projects at", new Date().toLocaleTimeString());

    // ✅ مثال: لو الموقع يرد بنجاح، أرسل تنبيه لتليجرام
    bot.sendMessage(
      CHAT_ID,
      `✅ تم فحص مشروع سكني بنجاح (${new Date().toLocaleTimeString()})\n${url}`
    );
  } catch (error) {
    console.error("❌ خطأ أثناء الفحص:", error.message);
    bot.sendMessage(
      CHAT_ID,
      `⚠️ خطأ أثناء الفحص: ${error.message}`
    );
  }
}

// ⏱️ فحص كل 30 ثانية
setInterval(checkSakaniProjects, 30000);

// 🚀 تشغيل السيرفر
const PORT = process.env.PORT || 3000;
app.listen(PORT, () =>
  console.log(`✅ Server running on port ${PORT}`)
);
