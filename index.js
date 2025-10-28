import TelegramBot from "node-telegram-bot-api";
import express from "express";
import axios from "axios";

// إعداداتك الخاصة
const token = "8497253482:AAH8z9Ib6x5K3oUllKXbejWDUNsBBu9Foco";
const CHAT_ID = "1244229957";

const bot = new TelegramBot(token, { polling: true });
const app = express();

// تأكيد أن البوت شغال
app.get("/", (req, res) => res.send("✅ Bot is running and checking Sakani projects..."));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

// قائمة المخططات (أضف كل أرقام المشاريع هنا)
const projects = [146, 229, 203]; // ← تقدر تضيف باقي المخططات هنا

async function checkProjects() {
  try {
    for (const id of projects) {
      const res = await axios.get(`https://sakani.sa/app/land-projects/${id}`);
      if (res.status === 200) {
        console.log(`✅ المشروع ${id} متاح`);
      }
    }
  } catch (err) {
    console.error("خطأ أثناء الفحص:", err.message);
  }
}

// فحص كل 30 ثانية
setInterval(checkProjects, 30000);
