import TelegramBot from "node-telegram-bot-api";
import express from "express";
import axios from "axios";

// === إعداداتك الخاصة ===
const token = "8497253482:AAH8z9Ib6x5K3oUllKXbejWDUNsBBu9Foco"; // ← توكن البوت
const CHAT_ID = 1244229957; // ← معرفك في التليجرام

// إنشاء البوت
const bot = new TelegramBot(token, { polling: true });
const app = express();

app.get("/", (req, res) => res.send("✅ Bot is running and watching Sakani projects..."));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

// 🟢 دالة جلب جميع المشاريع المجانية
async function fetchFreeProjects() {
  try {
    const res = await axios.get("https://sakani.sa/app/land-projects");
    const html = res.data;
    const regex = /https:\/\/sakani\.sa\/app\/land-projects\/\d+/g;
    const matches = html.match(regex);
    return [...new Set(matches)];
  } catch (err) {
    console.error("خطأ في جلب المشاريع:", err.message);
    return [];
  }
}

// 🟢 دالة فحص حالة القطع داخل كل مشروع
async function checkProjects() {
  const projects = await fetchFreeProjects();
  if (!projects.length) return;

  for (const project of projects) {
    try {
      const res = await axios.get(project);
      const html = res.data;

      // نبحث عن روابط القطع
      const regex = /https:\/\/sakani\.sa\/app\/units\/\d+/g;
      const units = html.match(regex);

      if (units && units.length > 0) {
        // مثال بسيط: لو لقينا قطعة جديدة نرسل تنبيه
        bot.sendMessage(
          CHAT_ID,
          `📢 تم تحديث المخطط:\n${project}\n📌 يحتوي على ${units.length} قطعة متاحة.`
        );
      }
    } catch (err) {
      console.error("خطأ أثناء فحص المشروع:", project, err.message);
    }
  }
}

// 🕒 فحص كل 30 ثانية
setInterval(checkProjects, 30 * 1000);

// 🔹 أوامر البوت في التليجرام
bot.onText(/\/start/, (msg) => {
  bot.sendMessage(
    msg.chat.id,
    `👋 أهلًا ${msg.chat.first_name}\nأنا أراقب جميع المخططات المجانية في سكني كل 30 ثانية وأرسل لك أي تحديث تلقائيًا 🏡`
  );
});

bot.onText(/\/check/, async (msg) => {
  bot.sendMessage(msg.chat.id, "⏳ جاري الفحص الآن...");
  await checkProjects();
  bot.sendMessage(msg.chat.id, "✅ تم الفحص وإرسال أي تحديثات جديدة.");
});
