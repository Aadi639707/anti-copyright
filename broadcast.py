import time
from pyrogram import filters
from pyrogram.errors import FloodWait

def register_broadcast(app, owner_ids, broadcast_list):
    @app.on_message(filters.command("broadcast") & filters.user(owner_ids))
    async def broadcast_command(client, message):
        if not message.reply_to_message:
            return await message.reply_text("Please reply to a message to broadcast it.")
        
        status_msg = await message.reply_text("Broadcast started...")
        success, failed = 0, 0
        
        for chat_id in list(broadcast_list):
            try:
                await message.reply_to_message.copy(chat_id)
                success += 1
                time.sleep(0.05)
            except FloodWait as e:
                time.sleep(e.value)
                try:
                    await message.reply_to_message.copy(chat_id)
                    success += 1
                except Exception:
                    failed += 1
            except Exception:
                failed += 1
                
        await status_msg.edit_text(f"Broadcast completed.\nSuccess: {success}\nFailed: {failed}")
      
