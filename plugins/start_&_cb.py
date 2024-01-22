import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery, Message, InputMediaPhoto

from helper.database import db
from config import Config, Txt  

@Client.on_message(filters.command("addadmin") & filters.user(Config.ADMIN))
async def add_admin(client, message):
    if len(message.command) > 1:
        user_id = int(message.command[1])
        await db.add_admin(user_id)
        await message.reply_text(f"User {user_id} has been added as an admin.")
    else:
        await message.reply_text("Please provide the user's ID to add them as an admin.")

@Client.on_message(filters.command("rmadmin") & filters.user(Config.ADMIN))
async def remove_admin(client, message):
    if len(message.command) > 1:
        user_id = int(message.command[1])
        await db.remove_admin(user_id)
        await message.reply_text(f"User {user_id} has been removed as an admin.")
    else:
        await message.reply_text("Please provide the user's ID to remove them as an admin.")

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user = message.from_user
    await db.add_user(client, message)                
    button = InlineKeyboardMarkup([[
      InlineKeyboardButton("ᴄᴏᴍᴍᴀɴᴅs", callback_data='commands')
    ],[
      InlineKeyboardButton('ᴜᴘᴅᴀᴛᴇs', url='https://t.me/Ani_Bots_Updates'),
      InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ', url='https://t.me/Anime_Sensei_Chat')
    ],[
      InlineKeyboardButton('ʜᴇʟᴘ', callback_data='about'),
      InlineKeyboardButton('ᴘʀᴇᴍɪᴜᴍ', callback_data='premium')
    ]])
    if Config.START_PIC:
        await message.reply_photo(Config.START_PIC, caption=Txt.START_TXT.format(user.mention), reply_markup=button)       
    else:
        await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)   

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    user_id = query.from_user.id  
    
    if data == "start":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("ᴄᴏᴍᴍᴀɴᴅs", callback_data='commands')
                ],[
                InlineKeyboardButton('ᴜᴘᴅᴀᴛᴇs', url='https://t.me/Ani_Bots_Updates'),
                InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ', url='https://t.me/Ani_Bots_Updates')
                ],[
                InlineKeyboardButton('ʜᴇʟᴘ', callback_data='about'),
                InlineKeyboardButton('ᴘʀᴇᴍɪᴜᴍ', callback_data='premium')
            ]])
        )
    elif data == "premium":
        await query.message.edit_text(
            text=Txt.PREMIUM_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton('ʙᴜʏ ɴᴏᴡ⚡', url='https://t.me/Sensei_Rimuru')
                ],[
                InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close"),
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="about")
            ]])            
        )
    elif data == "about":
        await query.message.edit_text(
            text=Txt.ABOUT_TXT.format(client.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("sᴇᴛᴜᴘ ᴀᴜᴛᴏʀᴇɴᴀᴍᴇ ғᴏʀᴍᴀᴛ", callback_data='file_names')
                ],[
                InlineKeyboardButton('ᴛʜᴜᴍʙɴᴀɪʟ', callback_data='thumbnail'),
                InlineKeyboardButton('sᴇǫᴜᴇɴᴄᴇ', url='https://t.me/RinNohara_xBot')
                ],[
                InlineKeyboardButton('ᴘʀᴇᴍɪᴜᴍ', callback_data='premium'),
                InlineKeyboardButton('ᴀʙᴏᴜᴛ', callback_data='about')
                ],[
                InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start')
            ]])
        )
    elif data == "commands":
        await query.message.edit_text(
            text=Txt.COMMANDS_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="close"),
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="start")
            ]])          
        )
    
    elif data == "file_names":
        format_template = await db.get_format_template(user_id)
        await query.message.edit_text(
            text=Txt.FILE_NAME_TXT.format(format_template=format_template),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="close"),
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="about")
            ]])
        )      
    
    elif data == "thumbnail":
        user_thumbnail = await db.get_thumbnail(user_id)
        
        await query.message.edit_media(
            media=InputMediaPhoto(user_thumbnail),
        )
        await query.message.edit_caption(
            caption=Txt.THUMB_TXT,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close"),
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="about"),
            ]]),
        )
    
    
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()
