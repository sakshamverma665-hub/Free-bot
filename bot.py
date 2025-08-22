import requests
import json
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# --- CONFIG ---
BOT_TOKEN = "8223755243:AAF8qhffdOHnFGmSHQd6ugcY7hcNC9Eqxuk"

# --- START COMMAND ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\nSend me a number (e.g. 987654321) and I will fetch details for you."
    )

# --- HANDLE NUMBER ---
async def handle_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    num = update.message.text.strip()

    if not num.isdigit():
        await update.message.reply_text("❌ Please send a valid number.")
        return

    url = f"https://xploide.site/Api.php?num={num}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error fetching data:\n{str(e)}")
        return

    # Add owner field
    if isinstance(data, dict):
        data["owner"] = "@Saksham24_11"
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                item["owner"] = "@Saksham24_11"

    # Pretty JSON
    pretty_json = json.dumps(data, indent=4, ensure_ascii=False)

    # Send as code block
    await update.message.reply_text(f"```json\n{pretty_json}\n```", parse_mode="Markdown")

# --- MAIN ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_number))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()