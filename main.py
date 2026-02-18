import os
import random
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN not set")

WORDS = ["python", "tiger", "planet", "rocket", "dragon"]

# ---------------- START ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.setdefault("score", 0)
    await update.message.reply_text(
        "🎮 Welcome to Fun Game Bot!\n\n"
        "Commands:\n"
        "/guess  → Number game\n"
        "/scramble → Word game\n"
        "/profile → Your score"
    )

# ---------------- PROFILE ----------------

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    score = context.user_data.get("score", 0)
    await update.message.reply_text(f"🏆 Your Score: {score}")

# ---------------- NUMBER GAME ----------------

async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(1, 20)
    context.user_data["number"] = number
    await update.message.reply_text("🎲 Guess a number between 1–20")

# ---------------- WORD SCRAMBLE ----------------

async def scramble(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word = random.choice(WORDS)
    scrambled = "".join(random.sample(word, len(word)))
    context.user_data["word"] = word
    await update.message.reply_text(f"🧩 Unscramble this word:\n{scrambled}")

# ---------------- MESSAGE HANDLER ----------------

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    # Number game check
    if "number" in context.user_data:
        try:
            guess = int(text)
            if guess == context.user_data["number"]:
                context.user_data["score"] += 1
                await update.message.reply_text("🔥 Correct! +1 Score")
                del context.user_data["number"]
            else:
                await update.message.reply_text("❌ Wrong! Try again")
        except:
            await update.message.reply_text("Send a valid number")
        return

    # Word game check
    if "word" in context.user_data:
        if text == context.user_data["word"]:
            context.user_data["score"] += 1
            await update.message.reply_text("🔥 Correct Word! +1 Score")
            del context.user_data["word"]
        else:
            await update.message.reply_text("❌ Wrong word, try again")
        return

    await update.message.reply_text("Use /guess or /scramble")

# ---------------- MAIN ----------------

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("guess", guess))
app.add_handler(CommandHandler("scramble", scramble))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🔥 Game Bot Started")
app.run_polling()

