from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from helper.database import db
from config import Txt


ON = [[InlineKeyboardButton('Metadata On ✅', callback_data='metadata_1')], [
    InlineKeyboardButton('Set Custom Metadata', callback_data='cutom_metadata')]]
OFF = [[InlineKeyboardButton('Metadata Off ❌', callback_data='metadata_0')], [
    InlineKeyboardButton('Set Custom Metadata', callback_data='cutom_metadata')]]


@Client.on_message(filters.private & filters.command('metadata'))
async def handle_metadata(bot: Client, message: Message):

    ms = await message.reply_text("**Please Wait...**", reply_to_message_id=message.id)
    bool_metadata = await db.get_metadata(message.from_user.id)
    user_metadata = await db.get_metadata_code(message.from_user.id)
    await ms.delete()
    if bool_metadata:

        return await message.reply_text(f"Your Current Metadata:-\n\n➜ `{user_metadata}` ", reply_markup=InlineKeyboardMarkup(ON))

    return await message.reply_text(f"Your Current Metadata:-\n\n➜ `{user_metadata}` ", reply_markup=InlineKeyboardMarkup(OFF))


