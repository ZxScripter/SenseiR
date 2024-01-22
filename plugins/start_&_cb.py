from pyrogram import Client as app, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaVideo, CallbackQuery

from helper.database import db
from config import Config, Txt
from helper.maindb import MaintenanceManager

maintenance_manager = MaintenanceManager()
maintenance_check_wrapper = maintenance_manager.maintenance_mode_check

@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user = message.from_user
    await db.add_user(client, message)
    
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("Commands", callback_data='commands')],
        [InlineKeyboardButton('Updates', url='https://t.me/UchihaPoliceUpdates'),
         InlineKeyboardButton('Support', url='https://t.me/UchihaPolice_Support')],
        [InlineKeyboardButton('Help', callback_data='about')]
    ])

    if Config.START_PIC:
        await message.reply_video(Config.START_PIC, caption=Txt.START_TXT.format(user.mention), reply_markup=button)
    else:
        await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)

@app.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id

    if data == "start":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Commands", callback_data='commands')],
                [InlineKeyboardButton('Updates', url='https://t.me/UchihaPoliceUpdates'),
                 InlineKeyboardButton('Support', url='https://t.me/UchihaPolice_Support')],
                [InlineKeyboardButton('Help', callback_data='about')]
            ])
        )
    elif data == "about":
        media = InputMediaVideo(Config.START_PIC)

        await query.message.edit_media(media=media)
        await query.message.edit_caption(
            caption=Txt.ABOUT_TXT.format(client.mention),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Set Username Format", callback_data='file_names')],
                [InlineKeyboardButton('Thumbnail', callback_data='thumbnail'),
                 InlineKeyboardButton('Sequence', callback_data='sequence')],
                [InlineKeyboardButton('Home', callback_data='start')]
            ])
        )
    elif data == "sequence":
        await query.message.edit_text(
            text=Txt.SEQUENCE_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Rɪɴ Nᴏʜᴀʀᴀ", url='https://t.me/RinNohara_xBot')],
                [InlineKeyboardButton("Close", callback_data="close"),
                 InlineKeyboardButton("Back", callback_data="start")]
            ])
        )
    elif data == "commands":
        await query.message.edit_text(
            text=Txt.COMMANDS_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Close", callback_data="close"),
                 InlineKeyboardButton("Back", callback_data="start")]
            ])
        )
    elif data == "file_names":
        format_template = await db.get_format_template(user_id)
        await query.message.edit_text(
            text=Txt.FILE_NAME_TXT.format(format_template=format_template),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Close", callback_data="close"),
                 InlineKeyboardButton("Back", callback_data="about")]
            ])
        )
    elif data == "thumbnail":
        user_thumbnail = await db.get_thumbnail(user_id)

        if user_thumbnail:
            await query.message.edit_media(media=InputMediaPhoto(user_thumbnail))
        else:
            await query.message.edit_text(text=Txt.THUMB_TXT, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Close", callback_data="close"),
                 InlineKeyboardButton("Back", callback_data="about")]
            ]))
        await query.message.edit_caption(
            caption=Txt.THUMB_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Close", callback_data="close"),
                 InlineKeyboardButton("Back", callback_data="about")]
            ])
        )
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except Exception as e:
            print(f"Error deleting message: {e}")
            await query.message.delete()
            await query.message.continue_propagation()
