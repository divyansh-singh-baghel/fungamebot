from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import random

TOKEN = "YOUR_BOT_TOKEN_HERE"

app = Flask(__name__)
bot = Bot(token=TOKEN)
application = ApplicationBuilder().token(TOKEN).build()

# ----- WORD LIST (5 LETTER WORDS) -----
WORDS = ["luffy", "narut", "zorro", "apple", "stone", "tiger"]

# ---------- COMMANDS ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hey! Main fun gaming bot hoon 😄\n\n"
        "🎲 Number Game → /game\n"
        "🧩 Guess the Word → /wordgame\n"
        "💬 Ya normal chat bhi kar sakte ho"
    )

# ----- NUMBER GAME -----
async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(1, 10)
    context.user_data["number"] = number
    context.user_data.pop("word", None)
    await update.message.reply_text(
        "🎲 Maine 1–10 ke beech ek number socha hai.\nGuess karo 👀"
    )

# ----- WORD GAME -----
async def wordgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word = random.choice(WORDS)
    context.user_data["word"] = word
    context.user_data.pop("number", None)
    await update.message.reply_text(
        "🧩 Guess the 5-letter WORD!\n"
        "Example: luffy\n\nType your guess 👇"
    )

# ---------- MESSAGE HANDLER ----------

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    # 🎲 Number Game Logic
    if "number" in context.user_data:
        try:
            guess = int(text)
            correct = context.user_data["number"]

            if guess == correct:
                await update.message.reply_text(
                    f"🔥 Sahi jawab! Number tha {correct} 😎"
                )
                del context.user_data["number"]
            else:
                await update.message.reply_text("❌ Galat 😅 dobara try karo")
        except:
            await update.message.reply_text("👀 Sirf number bhejo (1–10)")
        return

    # 🧩 Word Game Logic
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
            await update.message.reply_text(
                f"🎉 Jeet gaye bhai! Word tha **{word}** 🔥"
            )
            del context.user_data["word"]
        else:
            await update.message.reply_text(
                f"Result:\n{result}\n\nTry again 👀"
            )
        return

    # 💬 Normal Chat
    replies = [
        "😄 Haha",
        "🎮 Game khelna hai? /game ya /wordgame",
        "🤖 Main yahin hoon",
        "🔥 Mast!",
        "👋 Hello ji"
    ]
    await update.message.reply_text(random.choice(replies))


# ---------- WEBHOOK ----------

@app.route("/webhook", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    await application.process_update(update)
    return "ok"

@app.route("/")
def home():
    return "Bot is running 🚀"

# ---------- HANDLERS ----------
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("game", game))
application.add_handler(CommandHandler("wordgame", wordgame))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
