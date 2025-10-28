import TelegramBot from "node-telegram-bot-api";
import express from "express";
import axios from "axios";

// 🔐 بياناتك الخاصة
const token = "8497253482:AAH8z9Ib6x5K3oUllKXbejWDUNsBBu9Foco"; // توكن البوت
const CHAT_ID = "1244229957"; // معرفك في التليجرام

// ⚙️ إعداد البوت والخادم
const bot = new TelegramBot(token, { polling: true });
const app = express();

app.get("/", (req, res) => {
  res.send("✅ Bot is running and watching Sakani projects...");
});

// ✅ اختبار البوت
bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id, "مرحباً 👋 البوت يعمل الآن بنجاح!");
});

bot.onText(/ping/, (msg) => {
  bot.sendMessage(msg.chat.id, "🏓 Pong! البوت متصل ويعمل تمام ✅");
});

// 🕓 هنا نضيف فحص المشاريع كل 30 ثانية (لاحقاً نفعّلها)
async function checkSakaniProjects() {
  try {
    const res = await axios.get("https://sakani.sa/app/land-projects/146");
    // هنا لاحقاً بنضيف استخراج الأراضي وإرسال التنبيه
    console.log("Checked Sakani projects at", new Date().toLocaleTimeString());
  } catch (error) {
    console.error("خطأ أثناء الفحص:", error.message);
  }
}

// فحص كل 30 ثانية
setInterval(checkSakaniProjects, 30000);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`✅ Server running on port ${PORT}`));
