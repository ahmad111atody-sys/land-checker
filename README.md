import TelegramBot from "node-telegram-bot-api";
import express from "express";

const token = "ضع_توكن_بوتك_هنا"; // 🔹 حط توكن البوت هنا

const bot = new TelegramBot(token, { polling: true });
const app = express();

bot.on("message", (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, "تم استلام رسالتك ✅");
});

app.get("/", (req, res) => {
  res.send("Bot is running ✅");
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log("Server is running on port", PORT);
});
