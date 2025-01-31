from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Bot Configuration
BOT_TOKEN = "YOUR_BOT_TOKEN"  # Replace with your bot token
OWNER_ID = "123456789"  # Replace with your Telegram ID
SUPPORT_CHANNEL = "https://t.me/yourchannel"  # Replace with your support channel link

# Font Styles
font_styles = {
    "Bold": {"a": "𝗮", "b": "𝗯", "c": "𝗰", "d": "𝗱", "e": "𝗲", "f": "𝗳", "g": "𝗴",
             "h": "𝗵", "i": "𝗶", "j": "𝗷", "k": "𝗸", "l": "𝗹", "m": "𝗺", "n": "𝗻",
             "o": "𝗼", "p": "𝗽", "q": "𝗾", "r": "𝗿", "s": "𝘀", "t": "𝘁", "u": "𝘂",
             "v": "𝘃", "w": "𝘄", "x": "𝘅", "y": "𝘆", "z": "𝘇"},
    "Italic": {"a": "𝘢", "b": "𝘣", "c": "𝘤", "d": "𝘥", "e": "𝘦", "f": "𝘧", "g": "𝘨",
               "h": "𝘩", "i": "𝘪", "j": "𝘫", "k": "𝘬", "l": "𝘭", "m": "𝘮", "n": "𝘯",
               "o": "𝘰", "p": "𝘱", "q": "𝘲", "r": "𝘳", "s": "𝘴", "t": "𝘵", "u": "𝘶",
               "v": "𝘷", "w": "𝘸", "x": "𝘹", "y": "𝘺", "z": "𝘻"},
}

# Decorations
decorations = {
    "Stars": {"prefix": "★·.·´¯`·.·★ ", "suffix": " ★·.·´¯`·.·★"},
    "Fire": {"prefix": "🔥⋆ ", "suffix": " ⋆🔥"},
    "Hearts": {"prefix": "❤️¨*•.¸¸❤️ ", "suffix": " ❤️¸¸.•*¨❤️"},
}

# Store user selections
user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message with buttons."""
    keyboard = [
        [InlineKeyboardButton("🔠 Select Font Style", callback_data="select_font")],
        [InlineKeyboardButton("🎨 Select Decoration", callback_data="select_deco")],
        [InlineKeyboardButton("ℹ️ Support", callback_data="support")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Welcome to Stylish Name Generator! Select an option below:", reply_markup=reply_markup)


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send owner and support channel info."""
    support_text = f"👑 *Owner ID:* `{OWNER_ID}`\n📢 *Support Channel:* [Join Here]({SUPPORT_CHANNEL})"
    await update.callback_query.message.edit_text(support_text, parse_mode="Markdown")


async def select_font(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show font options."""
    keyboard = [[InlineKeyboardButton(style, callback_data=f"font_{style}")] for style in font_styles.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.message.edit_text("🔠 Choose a font style:", reply_markup=reply_markup)


async def select_deco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show decoration options."""
    keyboard = [[InlineKeyboardButton(deco, callback_data=f"deco_{deco}")] for deco in decorations.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.message.edit_text("🎨 Choose a decoration:", reply_markup=reply_markup)


async def font_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save user's font selection."""
    query = update.callback_query
    font_choice = query.data.split("_")[1]
    user_data[query.from_user.id] = {"font": font_choice}

    await query.message.edit_text(f"✅ Font selected: *{font_choice}*\nNow choose a decoration!", parse_mode="Markdown")
    await select_deco(update, context)


async def deco_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save user's decoration selection and ask for name input."""
    query = update.callback_query
    deco_choice = query.data.split("_")[1]

    if query.from_user.id in user_data:
        user_data[query.from_user.id]["deco"] = deco_choice
    else:
        user_data[query.from_user.id] = {"deco": deco_choice}

    await query.message.edit_text(f"✅ Decoration selected: *{deco_choice}*\nNow send me your name!", parse_mode="Markdown")


async def generate_stylish_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate and send the stylish name."""
    user_id = update.message.from_user.id
    name = update.message.text

    if user_id not in user_data or "font" not in user_data[user_id] or "deco" not in user_data[user_id]:
        await update.message.reply_text("❌ Please select a font and decoration first using /start!")
        return

    font_choice = user_data[user_id]["font"]
    deco_choice = user_data[user_id]["deco"]

    styled_name = "".join(font_styles[font_choice].get(c, c) for c in name)
    final_name = f"{decorations[deco_choice]['prefix']}{styled_name}{decorations[deco_choice]['suffix']}"

    await update.message.reply_text(f"✨ Your Stylish Name ✨\n{final_name}")


def main():
    """Start the bot."""
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("support", support))
    app.add_handler(CallbackQueryHandler(select_font, pattern="^select_font$"))
    app.add_handler(CallbackQueryHandler(select_deco, pattern="^select_deco$"))
    app.add_handler(CallbackQueryHandler(font_selected, pattern="^font_"))
    app.add_handler(CallbackQueryHandler(deco_selected, pattern="^deco_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_stylish_name))

    app.run_polling()


if __name__ == "__main__":
    main()
