import logging

from telegram import (
    Update,
    LabeledPrice,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    PreCheckoutQueryHandler,
    filters
)

from config import TELEGRAM_TOKEN, PROXY_URL, OWNER, BOT_NAME

logging.basicConfig(level=logging.INFO)


# ---------------- UI STYLE ----------------

def header():
    return (
        f"🎧 {BOT_NAME}\n"
        "━━━━━━━━━━━━━━\n"
    )


# ---------------- START ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔎 Search music", switch_inline_query_current_chat="")],
        [InlineKeyboardButton("⭐ Support project", callback_data="donate")]
    ])

    await update.message.reply_text(
        header() +
        "Multi-platform music search engine\n\n"
        "Sources:\n"
        "• YouTube Music\n"
        "• SoundCloud\n"
        "• Bandcamp\n"
        "• MusicBrainz\n\n"
        "━━━━━━━━━━━━━━\n"
        f"👤 {OWNER}",
        reply_markup=keyboard
    )


# ---------------- SEARCH (clean UI) ----------------

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Use: /search <song name>")
        return

    query = " ".join(context.args)

    # здесь можно подключить твои сервисы
    fake_results = [
        "Øneheart — Snowfall",
        "Mr.Kitty — After Dark",
        "Ghost — Mary On A Cross"
    ]

    text = header()
    text += f"Search: {query}\n\n"

    for r in fake_results:
        text += f"🎵 {r}\n"

    text += "\n━━━━━━━━━━━━━━\n"
    text += f"Powered by {OWNER}"

    await update.message.reply_text(text)


# ---------------- DONATE ENTRY ----------------

async def donate_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Use: /donate 50")
        return

    try:
        amount = int(context.args[0])
    except:
        await update.message.reply_text("Enter number: /donate 50")
        return

    await context.bot.send_invoice(
        chat_id=update.effective_chat.id,
        title="Support Music Search Engine",
        description="Donate to support development",
        payload=f"donate_{amount}",
        provider_token="",  # ⭐ Stars ONLY
        currency="XTR",
        prices=[LabeledPrice("Support", amount)],
    )


# ---------------- PRECHECKOUT ----------------

async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.pre_checkout_query.answer(ok=True)


# ---------------- SUCCESS PAYMENT ----------------

async def success_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):

    payment = update.message.successful_payment

    await update.message.reply_text(
        header() +
        "⭐ Thank you for your support!\n\n"
        f"Received: {payment.total_amount} Stars\n\n"
        f"— {OWNER}"
    )


# ---------------- ABOUT ----------------

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 Developer", url="https://t.me/h1nchek")],
        [InlineKeyboardButton("⭐ Donate", callback_data="donate")]
    ])

    await update.message.reply_text(
        header() +
        "Clean music discovery tool\n"
        "Fast • Minimal • Multi-source\n\n"
        f"{OWNER}",
        reply_markup=keyboard
    )


# ---------------- UNKNOWN ----------------

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "❓ Unknown command\nUse /start"
    )


# ---------------- MAIN ----------------

def main():

    builder = Application.builder().token(TELEGRAM_TOKEN)

    if PROXY_URL:
        builder = builder.proxy(PROXY_URL)

    app = builder.build()

    # core commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("donate", donate_cmd))
    app.add_handler(CommandHandler("about", about))

    # payments (Stars)
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, success_payment))

    # fallback
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    print("🎧 Bot started clean version")
    app.run_polling()


if __name__ == "__main__":
    main()