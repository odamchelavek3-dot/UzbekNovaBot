import os
import logging
from dotenv import load_dotenv
from google import genai
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not BOT_TOKEN or not GEMINI_API_KEY:
    raise ValueError("BOT_TOKEN yoki GEMINI_API_KEY sozlanmagan")

client = genai.Client(api_key=GEMINI_API_KEY)

logging.basicConfig(level=logging.INFO)

MODEL = "gemini-2.5-flash"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Assalomu alaykum! Men UzbekNova AI.\n\n"
        "Savolingizni yozing. Men sizga yordam beraman!"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text

    try:
        response = await asyncio.to_thread(
            client.models.generate_content,
            model=MODEL,
            contents=message
        )

        await update.message.reply_text(response.text or "Javob topilmadi.")

    except Exception:
        logging.exception("Gemini xatosi")
        await update.message.reply_text(
            "Kechirasiz, hozir javob olishda xatolik yuz berdi."
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    app.run_polling()

if __name__ == "__main__":
    import asyncio
    main()
