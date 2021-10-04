from time import time
from datetime import datetime
from config import BOT_USERNAME, BOT_NAME, ASSISTANT_NAME, OWNER_NAME, UPDATES_CHANNEL, GROUP_SUPPORT
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from helpers.decorators import sudo_users_only


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_message(command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>✨ **Hey {message.from_user.first_name}** \n
💭 **ɪ'ᴍ [{BOT_NAME}](https://t.me/{BOT_USERNAME}) Allows you to play songs!

☑️ Find out all bot's  Commands By click on the help Inline button /help** [.](https://telegra.ph/file/42fa9676f01c6fd0e15bb.jpg)

</b>""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        "➕ Add me to group ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],[
                    InlineKeyboardButton(
                        " Setup⚡", callback_data="cbhowtouse")
                ],[
                    InlineKeyboardButton(
                        "⚒️ Bot List ⚒️", url="https://t.me/Bondofbestizz")
                ],[
                    InlineKeyboardButton(
                        "💡Support", url=f"https://t.me/electroBot_support"
                    ),
                    InlineKeyboardButton(
                        "🤖 Updates", url=f"https://t.me/electro_updates")
                ],[
                    InlineKeyboardButton(
                        " ℹ️ Help and Commands", callback_data="cbcmds"
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )


@Client.on_message(command(["start", f"start@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def start(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        f"""✅ **ᴢᴀɪᴅ ɪꜱ ʀᴜɴɴɪɴɢ**\n<b>💠 **ᴜᴘᴛɪᴍᴇ:**</b> `{uptime}`""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💡Support", url=f"https://t.me/Electrobot_SUPPORT"
                    ),
                    InlineKeyboardButton(
                        "🤖 Updates", url=f"https://t.me/Electro_updates"
                    )
                ]
            ]
        )
    )

@Client.on_message(command(["help", f"help@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_text(
        f"""<b>👋🏻 **Hello** {message.from_user.mention()}</b>

**Please press the button below to read the explanation and see the list of available commands powered By Zaid!**

⚡ __Powered by {BOT_NAME} electro""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="❔ How to use me", callback_data=f"cbguide"
                    )
                ]
            ]
        )
    )

@Client.on_message(command(["help", f"help@{BOT_USERNAME}"]) & filters.private & ~filters.edited)
async def help_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>💡 Hello {message.from_user.mention} welcome to the help menu !</b>

**in this menu you can open several available command menus, in each command menu there is also a brief explanation of each command**

⚡ __ᴘᴏᴡᴇʀᴇᴅ ʙʏ {BOT_NAME} Electro__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⚡ Basic Cmds", callback_data="cbbasic"
                    ),
                    InlineKeyboardButton(
                        " Advanced Cmds", callback_data="cbadvanced"
                    )
                ],
                [
                    InlineKeyboardButton(
                        " Admin Cmds", callback_data="cbadmin"
                    ),
                    InlineKeyboardButton(
                        " Sudo Cmds", callback_data="cbsudo"
                    )
                ],
                [
                    InlineKeyboardButton(
                        " Owner Cmds", callback_data="cbowner"
                    )
                ],
                [
                    InlineKeyboardButton(
                        " Fun Cmds", callback_data="cbfun"
                    )
                ]
            ]
        )
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text(" Pinging...")
    delta_ping = time() - start
    await m_reply.edit_text(
        " `Pong!!`\n"
        f"op  `{delta_ping * 1000:.3f} ᴍꜱ`"
    )


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 Electro:\n"
        f"• **Uptime:** `{uptime}`\n"
        f"• **Start time:** `{START_TIME_ISO}`"
    )
