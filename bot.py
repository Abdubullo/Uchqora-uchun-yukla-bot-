import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests

# Bot tokeningizni ENV variable orqali olamiz
import os
TOKEN = os.getenv("7539658089:AAGwBPqeyn_TQOk5UGkcrh3bm4VcOfVsRA0")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! 👋 Video yuklash uchun Instagram, YouTube yoki TikTok link yuboring.")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.reply_text("⏳ Video yuklanmoqda...")

    try:
        api_url = f"https://save-from.link/api/convert?url={url}"
        r = requests.get(api_url)
        data = r.json()

        video_url = data.get("url")
        if video_url:
            await update.message.reply_video(video=video_url, caption="✅ Yuklab berildi!")
        else:
            await update.message.reply_text("❌ Yuklab bo‘lmadi. Linkni tekshiring.")
    except Exception as e:
        await update.message.reply_text(f"Xatolik: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

app.run_polling()
