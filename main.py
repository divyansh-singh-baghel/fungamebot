import os
import random
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN not set in environment variables")

app = Flask(__name__)

WORDS = ["luffy", "narut", "zorro", "apple", "stone", "tiger"]

# -------- COMMANDS --------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hey! Fun Gaming Bot 😄\n\n"
        "🎲 /game\n"
        "🧩 /wordgame"
    )

async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["number"] = random.randint(1, 10)
    await update.message.reply_text("🎲 Guess number 1–10")

async def wordgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["word"] = random.choice(WORDS)
    await update.message.reply_text("🧩 Guess 5-letter word")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "number" in context.user_data:
        try:
            guess = int(text)
            correct = context.user_data["number"]
            if guess == correct:
                await update.message.reply_text("🔥 Correct!")
                del context.user_data["number"]
            else:
                await update.message.reply_text("❌ Try again")
        except:
            await update.message.reply_text("Send number only")
        return

    await update.message.reply_text("Use /game or /wordgame")

# -------- TELEGRAM BOT --------

async def run_bot():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("game", game))
    application.add_handler(CommandHandler("wordgame", wordgame))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🔥 Bot Started Successfully!")
    await application.run_polling()

# -------- FLASK ROUTE --------

@app.route("/")
def home():
    return "Bot Running 🚀"

# -------- MAIN --------

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    app.run(host="0.0.0.0", port=10000)
