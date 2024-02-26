from config import Config
from helper.database import db
from helper.admins import add_admin, is_admin, remove_admin, get_admin_list

from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
import os, sys, time, asyncio, logging, datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@Client.on_message(filters.private & filters.command("tutorial"))
async def tutioral_bot(b, m):
    await m.reply_text("Message Admin")

@Client.on_message(filters.command(["stats", "status"]))
async def get_stats(bot, message):
    user_id = message.from_user.id
    is_user_admin = await is_admin(user_id)
    if not is_user_admin and user_id not in Config.ADMIN:        
        return
    total_users = await db.total_users_count()
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - bot.uptime))    
    start_t = time.time()
    st = await message.reply('**Aᴄᴄᴇꜱꜱɪɴɢ Tʜᴇ Dᴇᴛᴀɪʟꜱ.....**')    
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await st.edit(text=f"**--Bᴏᴛ Sᴛᴀᴛᴜꜱ--** \n\n**⌚️ Bᴏᴛ Uᴩᴛɪᴍᴇ:** {uptime} \n**🐌 Cᴜʀʀᴇɴᴛ Pɪɴɢ:** `{time_taken_s:.3f} ᴍꜱ` \n**👭 Tᴏᴛᴀʟ Uꜱᴇʀꜱ:** `{total_users}`")

@Client.on_message(filters.command('auth') & filters.private)
async def add_admin_command(bot, message):
    user_id = message.from_user.id
    if user_id not in Config.ADMIN:
        await message.reply_text("Only Bot Owner can use this command.")
        return

    # Check if the command has the expected number of arguments
    if len(message.command) != 2:
        await message.reply_text("<b>Usage:</b> /auth userid")
        return
    try:
        user_id_to_add = int(message.command[1])
    except ValueError:
        await message.reply_text("Invalid user ID. Please provide a valid user ID.")
        return
    # Add the user to the admin list in the database
    added = await add_admin(user_id_to_add)
    if added:
        await message.reply_text(f"<b>User {user_id_to_add} has been added to the admin list.</b>")
    else:
        await message.reply_text(f"<b>User {user_id_to_add} is already an admin.</b>")
        

@Client.on_message(filters.command('unauth') & filters.private)
async def remove_admin_command(bot, message):
    user_id = message.from_user.id
    if user_id != Config.ADMIN:
        await message.reply_text("Only Bot Owner can use this command.")
        return
    # Check if the command has the expected number of arguments
    if len(message.command) != 2:
        await message.reply_text("<b>Usage:</b> /unauth userid")
        return
    try:
        user_id_to_remove = int(message.command[1])
    except ValueError:
        await message.reply_text("Invalid user ID. Please provide a valid user ID.")
        return
    # Remove the user from the admin list in the database
    removed = await remove_admin(user_id_to_remove)
    if removed:
        await message.reply_text(f"<b>User {user_id_to_remove} has been removed from the admin list.</b>")
    else:
        await message.reply_text(f"<b>User {user_id_to_remove} is not an admin or was not found in the admin list.</b>")


@Client.on_message(filters.command('authorised') & filters.private)
async def admin_list_command(bot, message):
    user_id = message.from_user.id
    is_user_admin = await is_admin(user_id)
    if not is_user_admin and user_id not in Config.ADMIN:
        await message.reply_text("Only Bot Owner and Admins can use this command.")
        return

    admin_user_ids = await get_admin_list()  
    formatted_admins = []

    for admin_id in admin_user_ids:
        try:
            user = await bot.get_users(admin_id)
            if user:
                username = user.username
                full_name = user.first_name if user.first_name else "" 
                full_name += " " + user.last_name if user.last_name else ""  
                full_name = full_name.strip() 

                if username:
                    profile_link = f"{full_name} - @{username}"
                else:
                    profile_link = full_name
                formatted_admins.append(profile_link)
        except Exception as e:
            print(f"Error fetching user: {e}")

    if formatted_admins:
        admins_text = "\n".join(formatted_admins)
        text = f"<b>Admin Users:</b>\n\n{admins_text}"
    else:
        text = "<b>No admin users found.</b>"

    await message.reply_text(text, disable_web_page_preview=True)
    

#Restart to cancell all process 
@Client.on_message(filters.private & filters.command("restart") & filters.user(Config.ADMIN))
async def restart_bot(b, m):
    await m.reply_text("__⚡ʀᴇꜱᴛᴀʀᴛɪɴɢ.....__")
    os.execl(sys.executable, sys.executable, *sys.argv)


@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMIN) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    await bot.send_message(Config.LOG_CHANNEL, f"{m.from_user.mention} or {m.from_user.id} Iꜱ ꜱᴛᴀʀᴛᴇᴅ ᴛʜᴇ Bʀᴏᴀᴅᴄᴀꜱᴛ......")
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text("Bʀᴏᴀᴅᴄᴀꜱᴛ Sᴛᴀʀᴛᴇᴅ..!") 
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    total_users = await db.total_users_count()
    async for user in all_users:
        sts = await send_msg(user['_id'], broadcast_msg)
        if sts == 200:
           success += 1
        else:
           failed += 1
        if sts == 400:
           await db.delete_user(user['_id'])
        done += 1
        if not done % 20:
           await sts_msg.edit(f"Bʀᴏᴀᴅᴄᴀꜱᴛ Iɴ Pʀᴏɢʀᴇꜱꜱ: \nTᴏᴛᴀʟ Uꜱᴇʀꜱ {total_users} \nCᴏᴍᴩʟᴇᴛᴇᴅ: {done} / {total_users}\nSᴜᴄᴄᴇꜱꜱ: {success}\nFᴀɪʟᴇᴅ: {failed}")
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(f"Bʀᴏᴀᴅᴄᴀꜱᴛ Cᴏᴍᴩʟᴇᴛᴇᴅ: \nCᴏᴍᴩʟᴇᴛᴇᴅ Iɴ `{completed_in}`.\n\nTᴏᴛᴀʟ Uꜱᴇʀꜱ {total_users}\nCᴏᴍᴩʟᴇᴛᴇᴅ: {done} / {total_users}\nSᴜᴄᴄᴇꜱꜱ: {success}\nFᴀɪʟᴇᴅ: {failed}")
           
async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        logger.info(f"{user_id} : Dᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ")
        return 400
    except UserIsBlocked:
        logger.info(f"{user_id} : Bʟᴏᴄᴋᴇᴅ Tʜᴇ Bᴏᴛ")
        return 400
    except PeerIdInvalid:
        logger.info(f"{user_id} : Uꜱᴇʀ Iᴅ Iɴᴠᴀʟɪᴅ")
        return 400
    except Exception as e:
        logger.error(f"{user_id} : {e}")
        return 500
 
