import time
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from broadcast import register_broadcast

# ----------------- CONFIGURATION -----------------
API_ID = 1234567               # Apna Telegram API ID daalein (Integer)
API_HASH = "your_api_hash"     # Apna Telegram API Hash daalein
BOT_TOKEN = "your_bot_token"   # BotFather wala Token daalein
BOT_USERNAME = "CopyrightRestrictBot" 

OWNER_IDS = [8985254350]       
START_IMAGE = "https://files.catbox.moe/0etszd.jpg"

app = Client("PremiumAntiCopyrightBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

approved_users = {} 
broadcast_list = set() 

# Register broadcast from separate file
register_broadcast(app, OWNER_IDS, broadcast_list)

# ----------------- FONT CONVERTER (SMALL CAPS) -----------------
SMALL_CAPS = {
    'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ',
    'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ', 'q': 'Q', 'r': 'ʀ',
    's': 'ꜱ', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ',
    'A': 'ᴀ', 'B': 'ʙ', 'C': 'ᴄ', 'D': 'ᴅ', 'E': 'ᴇ', 'F': 'ꜰ', 'G': 'ɢ', 'H': 'ʜ', 'I': 'ɪ',
    'J': 'ᴊ', 'K': 'ᴋ', 'L': 'ʟ', 'M': 'ᴍ', 'N': 'ɴ', 'O': 'ᴏ', 'P': 'ᴘ', 'Q': 'Q', 'R': 'ʀ',
    'S': 'ꜱ', 'T': 'ᴛ', 'U': 'ᴜ', 'V': 'ᴠ', 'W': 'ᴡ', 'X': 'x', 'Y': 'ʏ', 'Z': 'ᴢ'
}

def font(text: str) -> str:
    return "".join(SMALL_CAPS.get(c, c) for c in text)

# ----------------- HELPER FUNCTIONS -----------------
async def is_admin(client, message):
    if not message.from_user:
        if message.sender_chat and message.sender_chat.id == message.chat.id:
            return True
        return False
        
    if message.from_user.id in OWNER_IDS:
        return True
        
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
            return True
    except Exception:
        pass
    return False

async def extract_user(client, message):
    if message.entities:
        for entity in message.entities:
            if entity.type == enums.MessageEntityType.TEXT_MENTION:
                return entity.user.id, entity.user.first_name
            elif entity.type == enums.MessageEntityType.MENTION:
                username = message.text[entity.offset:entity.offset+entity.length]
                try:
                    user = await client.get_users(username)
                    return user.id, user.first_name
                except Exception:
                    pass

    if message.reply_to_message:
        if message.reply_to_message.from_user:
            return message.reply_to_message.from_user.id, message.reply_to_message.from_user.first_name

    if len(message.command) > 1:
        user_input = message.command[1]
        if user_input.isdigit():
            user_id = int(user_input)
            try:
                user = await client.get_users(user_id)
                return user.id, user.first_name
            except Exception:
                return user_id, f"User_{user_id}"
                
    return None, None

# ----------------- TEXT TEMPLATES -----------------
def get_start_text(first_name):
    return (
        f"👋 ᴡᴇʟᴄᴏᴍᴇ, {font(first_name)}!\n\n"
        "🛡️ ᴋᴇᴇᴘ ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘ ꜱᴀꜰᴇ ᴡɪᴛʜ ᴀɴᴛɪ-ᴄᴏᴘʏʀɪɢʜᴛ ʙᴏᴛ.\n\n"
        "🔒 ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇꜱ ᴜɴᴡᴀɴᴛᴇᴅ ᴍᴇᴅɪᴀ\n"
        "⚡ ʙʟᴏᴄᴋꜱ ꜰᴏʀᴡᴀʀᴅᴇᴅ ᴍᴇꜱꜱᴀɢᴇꜱ\n"
        "✅ ᴀᴘᴘʀᴏᴠᴀʟ ꜱʏꜱᴛᴇᴍ\n"
        "🚀 ꜰᴀꜱᴛ, ʀᴇʟɪᴀʙʟᴇ & ᴇᴀꜱʏ ᴛᴏ ᴜꜱᴇ\n\n"
        "ᴛᴀᴘ ʜᴇʟᴘ ᴛᴏ ᴠɪᴇᴡ ᴛʜᴇ ꜱᴇᴛᴜᴘ ɢᴜɪᴅᴇ, ꜰᴇᴀᴛᴜʀᴇꜱ, ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅꜱ."
    )

HELP_TEXT = (
    "🛠 **ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅꜱ**\n\n"
    "ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅ:\n"
    " ➪ /approve - ᴀᴘᴘʀᴏᴠᴇ ʙʏ ʀᴇᴘʟʏ, ᴜꜱᴇʀɴᴀᴍᴇ, ɪᴅ, ᴏʀ ᴛᴇxᴛ ᴛᴀɢ\n"
    " ➪ /unapprove - ᴜɴᴀᴘᴘʀᴏᴠᴇ ᴀ ᴜꜱᴇʀ ʙʏ ʀᴇᴘʟʏ, ᴜꜱᴇʀɴᴀᴍᴇ, ᴏʀ ɪᴅ\n"
    " ➪ /approvelist - ᴠɪᴇᴡ ᴀʟʟ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜꜱᴇʀꜱ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ\n\n"
    "ɢᴇɴᴇʀᴀʟ ᴄᴏᴍᴍᴀɴᴅ:\n"
    " ➪ /ping - ᴄʜᴇᴄᴋ ʙᴏᴛ ʟᴀᴛᴇɴᴄʏ\n"
    " ➪ /broadcast - (ᴏᴡɴᴇʀ ᴏɴʟʏ) ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴍᴇꜱꜱᴀɢᴇꜱ\n\n"
    "⚠️ ɴᴏᴛᴇ: ɪ ᴍᴜꜱᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴡɪᴛʜ 'ᴅᴇʟᴇᴛᴇ ᴍᴇꜱꜱᴀɢᴇꜱ' ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴡᴏʀᴋ ᴘʀᴏᴘᴇʀʟʏ."
)

def get_start_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [InlineKeyboardButton("📋 ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅꜱ", callback_data="help_menu")],
        [
            InlineKeyboardButton("👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ ↗️", url="https://t.me/PerksOwner"),
            InlineKeyboardButton("📢 ᴄʜᴀɴɴᴇʟ ↗️", url="https://t.me/PerkBots")
        ]
    ])

def get_help_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="start_menu")]])

# ----------------- START COMMAND -----------------
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    broadcast_list.add(message.chat.id)
    await message.reply_photo(
        photo=START_IMAGE,
        caption=get_start_text(message.from_user.first_name),
        reply_markup=get_start_keyboard()
    )

# ----------------- CALLBACK QUERIES -----------------
@app.on_callback_query(filters.regex("help_menu"))
async def help_callback(client, callback_query):
    await callback_query.message.edit_caption(caption=HELP_TEXT, reply_markup=get_help_keyboard())

@app.on_callback_query(filters.regex("start_menu"))
async def start_callback(client, callback_query):
    await callback_query.message.edit_caption(
        caption=get_start_text(callback_query.from_user.first_name),
        reply_markup=get_start_keyboard()
    )

# ----------------- PING COMMAND -----------------
@app.on_message(filters.command("ping"))
async def ping_command(client, message):
    start_time = time.time()
    reply = await message.reply_text("Pinging...")
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000)
    await reply.edit_text(f"Pong!\nLatency: {ping_time}ms")

# ----------------- ANTI-COPYRIGHT LOGIC -----------------
@app.on_message(filters.group & (filters.video | filters.photo | filters.forwarded))
async def anti_copyright_delete(client, message):
    chat_id = message.chat.id
    
    if await is_admin(client, message):
        return

    user_id = message.from_user.id if message.from_user else None
    if not user_id:
        return

    if chat_id in approved_users and user_id in approved_users[chat_id]:
        return

    try:
        await message.delete()
    except Exception:
        pass 

# ----------------- APPROVE / UNAPPROVE COMMANDS -----------------
@app.on_message(filters.command("approve") & filters.group)
async def approve_user(client, message):
    if not await is_admin(client, message):
        return await message.reply_text(font("You need to be an admin to use this command."))
        
    target_id, target_name = await extract_user(client, message)
    
    if not target_id:
        return await message.reply_text(font("Please reply to a user, tag them, or provide their ID/Username."))
        
    chat_id = message.chat.id
    if chat_id not in approved_users:
        approved_users[chat_id] = set()
        
    approved_users[chat_id].add(target_id)
    await message.reply_text(font(f"{target_name} ({target_id}) has been approved successfully."))

@app.on_message(filters.command("unapprove") & filters.group)
async def unapprove_user(client, message):
    if not await is_admin(client, message):
        return await message.reply_text(font("You need to be an admin to use this command."))
        
    target_id, target_name = await extract_user(client, message)
    
    if not target_id:
        return await message.reply_text(font("Please reply to a user, tag them, or provide their ID/Username."))
        
    chat_id = message.chat.id
    if chat_id in approved_users and target_id in approved_users[chat_id]:
        approved_users[chat_id].remove(target_id)
        await message.reply_text(font(f"{target_name} ({target_id}) has been unapproved."))
    else:
        await message.reply_text(font(f"{target_name} is not in the approved list."))

@app.on_message(filters.command("approvelist") & filters.group)
async def approvelist(client, message):
    if not await is_admin(client, message):
        return
        
    chat_id = message.chat.id
    if chat_id not in approved_users or not approved_users[chat_id]:
        return await message.reply_text(font("There are no approved users in this group."))
        
    text = "Approved Users:\n"
    for uid in approved_users[chat_id]:
        text += f"- `{uid}`\n"
        
    await message.reply_text(font(text))

if __name__ == "__main__":
    print("Bot is starting...")
    app.run()
      
