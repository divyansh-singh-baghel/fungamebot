
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import threading
import random

# 🔴 Apna REAL token daalna
TOKEN = "8581059074:AAHBAcRNQGcrt2WQhFjaB0PASccX5GOvrVM"

app = Flask(__name__)

# ----- WORD LIST -----
WORDS = ["luffy", "narut", "zorro", "apple", "stone", "tiger"]

# ---------- COMMANDS ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hey! Main Fun Gaming Bot hoon 😄\n\n"
        "🎲 Number Game → /game\n"
        "🧩 Guess the Word → /wordgame"
    )

# ----- NUMBER GAME -----
async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["number"] = random.randint(1, 10)
    context.user_data.pop("word", None)
    await update.message.reply_text("🎲 Guess number between 1–10")

# ----- WORD GAME -----
async def wordgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["word"] = random.choice(WORDS)
    context.user_data.pop("number", None)
    await update.message.reply_text("🧩 Guess the 5-letter word")

# ---------- MESSAGE HANDLER ----------

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    # 🎲 Number Game
    if "number" in context.user_data:
        try:
            guess = int(text)
            correct = context.user_data["number"]

            if guess == correct:
                await update.message.reply_text(f"🔥 Sahi jawab! Number tha {correct}")
                del context.user_data["number"]
            else:
                await update.message.reply_text("❌ Galat, dobara try karo")
        except:
            await update.message.reply_text("👀 Sirf number bhejo (1–10)")
        return

    # 🧩 Word Game
    if "word" in context.user_data:
        word = context.user_data["word"]

        if len(text) != 5:
            await update.message.reply_text("⚠️ Sirf 5-letter word likho")
            return

        result = ""
        for i in range(5):
            if text[i] == word[i]:
                result += f"✅ {text[i]}  "
            elif text[i] in word:
                result += f"⚠️ {text[i]}  "
            else:
                result += f"❌ {text[i]}  "

        if text == word:
            await update.message.reply_text(f"🎉 Jeet gaye! Word tha {word}")
            del context.user_data["word"]
        else:
            await update.message.reply_text(f"Result:\n{result}\n\nTry again 👀")
        return

    # 💬 Normal Chat
    await update.message.reply_text("🎮 Game khelna hai? /game ya /wordgame")

# ---------- RUN TELEGRAM BOT ----------

def run_bot():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("game", game))
    application.add_handler(CommandHandler("wordgame", wordgame))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🔥 Bot started successfully!")
    application.run_polling()

# ---------- Flask route (Render ke liye) ----------

@app.route("/")
def home():
    return "Bot is running 24/7 🚀"

# ---------- MAIN ----------

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
