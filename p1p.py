import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

BOT_TOKEN = "8694277322:AAGrfQyUFWgmRQ3NPzSrN83SgNdNzSQ4qsE"
ADMIN_ID = 1484173564

channels = []  # [{"id": -100xxxx, "link": "https://t.me/+xxxx"}]

IMAGE_URL = "https://files.catbox.moe/wcfmqd.jpg"


# 🔑 KEY
def generate_key():
    return str(random.randint(1000000000, 9999999999))


# 🔍 CHECK ALL CHANNEL JOIN
async def check_all_join(user_id, bot):
    for ch in channels:
        try:
            member = await bot.get_chat_member(ch["id"], user_id)

            # ❌ not joined
            if member.status in ["left", "kicked"]:
                return False

        except:
            return False

    return True


# 🚀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []

    for i, ch in enumerate(channels, start=1):
        keyboard.append([InlineKeyboardButton(f"Join Channel {i} 🔥", url=ch["link"])])

    keyboard.append([InlineKeyboardButton("✅ VERIFY", callback_data="verify")])

    await update.message.reply_photo(
        photo=IMAGE_URL,
        caption="""
👻 Sab channels join karo phir VERIFY dabao

𝗛𝗲𝗹𝗹𝗼 𝗨𝘀𝗲𝗿 👻 𝐁𝐎𝐓

ALL CHANNEL JOIN 🥰

𝐇𝐎𝐖 𝐓𝐎 𝐆𝐄𝐍𝐄𝐑𝐀𝐓𝐄 𝐊𝐄𝐘 💀
<a href="https://t.me/setupchanel_0/60">𝐂𝐋𝐈𝐂𝐊 𝐇𝐄𝐑𝐄</a>
""",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ✅ VERIFY
async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    ok = await check_all_join(user_id, context.bot)

    if not ok:
        await query.message.reply_text("❌ Sab channel join karo fir VERIFY dabao")
        return

    key = generate_key()

    await query.message.reply_text(
        f"""
🔑 Key - {key}

📥 DRIP SCINET APK:
https://www.mediafire.com/file/if3uvvwjbj87lo2/DRIPCLIENT_v6.2_GLOBAL_AP.apks/file

⚠️ APK ke baad join karo:
https://t.me/+MkNcxGuk-w43MzBl
"""
    )


# 👑 ADMIN PANEL
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    keyboard = [
        [InlineKeyboardButton("➕ Add Channel", callback_data="add")],
        [InlineKeyboardButton("➖ Remove Channel", callback_data="remove")],
        [InlineKeyboardButton("📋 List Channels", callback_data="list")]
    ]

    await update.message.reply_text("Admin Panel ⚙️", reply_markup=InlineKeyboardMarkup(keyboard))


# ➕ ADD
async def add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text(
        "Send:\n-1001234567890 https://t.me/+link"
    )
    context.user_data["mode"] = "add"


# ➖ REMOVE
async def remove_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text("Send channel ID")
    context.user_data["mode"] = "remove"


# 📋 LIST
async def list_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not channels:
        await update.callback_query.message.reply_text("No channels")
        return

    text = "\n".join([f"{c['id']} → {c['link']}" for c in channels])
    await update.callback_query.message.reply_text(text)


# 💬 HANDLE ADMIN INPUT
async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    mode = context.user_data.get("mode")

    if mode == "add":
        try:
            cid, link = update.message.text.split()
            channels.append({"id": int(cid), "link": link})
            await update.message.reply_text("✅ Channel Added")
        except:
            await update.message.reply_text("❌ Format wrong")

    elif mode == "remove":
        try:
            cid = int(update.message.text)
            channels[:] = [c for c in channels if c["id"] != cid]
            await update.message.reply_text("❌ Removed")
        except:
            await update.message.reply_text("Error")

    context.user_data["mode"] = None


# 🔘 BUTTON
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query.data == "verify":
        await verify(update, context)

    elif query.data == "add":
        await add_channel(update, context)

    elif query.data == "remove":
        await remove_channel(update, context)

    elif query.data == "list":
        await list_channel(update, context)


# 🚀 RUN
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))

print("Bot Running...")
app.run_polling()
