from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InputMediaDocument, Message 
from PIL import Image
from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.utils import progress_for_pyrogram, humanbytes, convert
from helper.database import db
from helper.admins import is_admin
from config import Config
import os
import time
import re
import asyncio

renaming_operations = {}
file_count_limit = 100
sleep_duration = 20 * 60 

if not os.path.isdir("Metadata"):
        os.mkdir("Metadata")
    
user_file_counts = {}

pattern1 = re.compile(r'S(\d+)(?:E|EP)(\d+)')
pattern2 = re.compile(r'S(\d+)\s*(?:E|EP|-\s*EP)(\d+)')
pattern3 = re.compile(r'(?:[([<{]?\s*(?:E|EP)\s*(\d+)\s*[)\]>}]?)')
pattern3_2 = re.compile(r'(?:\s*-\s*(\d+)\s*)')
pattern4 = re.compile(r'S(\d+)[^\d]*(\d+)', re.IGNORECASE)
patternX = re.compile(r'(\d+)')
pattern5 = re.compile(r'\b(?:.*?(\d{3,4}[^\dp]*p).*?|.*?(\d{3,4}p))\b', re.IGNORECASE)
pattern6 = re.compile(r'[([<{]?\s*4k\s*[)\]>}]?', re.IGNORECASE)
pattern7 = re.compile(r'[([<{]?\s*2k\s*[)\]>}]?', re.IGNORECASE)
pattern8 = re.compile(r'[([<{]?\s*HdRip\s*[)\]>}]?|\bHdRip\b', re.IGNORECASE)
pattern9 = re.compile(r'[([<{]?\s*4kX264\s*[)\]>}]?', re.IGNORECASE)
pattern10 = re.compile(r'[([<{]?\s*4kx265\s*[)\]>}]?', re.IGNORECASE)

def extract_quality(filename):
    match5 = re.search(pattern5, filename)
    if match5:
        quality5 = match5.group(1) or match5.group(2)
        return quality5

    match6 = re.search(pattern6, filename)
    if match6:
        return "4k"

    match7 = re.search(pattern7, filename)
    if match7:
        return "2k"

    match8 = re.search(pattern8, filename)
    if match8:
        return "HdRip"

    match9 = re.search(pattern9, filename)
    if match9:
        return "4kX264"

    match10 = re.search(pattern10, filename)
    if match10:
        return "4kx265"

    return "Unknown"

def extract_episode_number(filename):    
    match = re.search(pattern1, filename)
    if match:
        return match.group(2)

    match = re.search(pattern2, filename)
    if match:
        return match.group(2)

    match = re.search(pattern3, filename)
    if match:
        return match.group(1)

    match = re.search(pattern3_2, filename)
    if match:
        return match.group(1)

    match = re.search(pattern4, filename)
    if match:
        return match.group(2)

    match = re.search(patternX, filename)
    if match:
        return match.group(1)

    return None

@Client.on_message(filters.private & filters.command("format"))
async def auto_rename_command(client, message):
    user_id = message.from_user.id
    format_template = message.text.split("/format", 1)[1].strip()
    await db.set_format_template(user_id, format_template)
    await message.reply_text("ʀᴇɴᴀᴍᴇ ғᴏʀᴍᴀᴛ ᴜᴘᴅᴀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!")

@Client.on_message(filters.private & filters.command("setmedia"))
async def set_media_command(client, message):
    user_id = message.from_user.id
    media_type = message.text.split("/setmedia", 1)[1].strip().lower()
    await db.set_media_preference(user_id, media_type)
    await message.reply_text(f"Media preference set to: {media_type}")
@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def auto_rename_files(client, message):    
    user_id = message.from_user.id
    firstname = message.from_user.first_name
    is_user_admin = await is_admin(user_id)
    if not is_user_admin and user_id not in Config.ADMIN:        
        await message.reply_text("Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪsᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ ! Cᴏɴᴛᴀᴄᴛ:- @Sensei_Rimuru")
        return    

    format_template = await db.get_format_template(user_id)
    media_preference = await db.get_media_preference(user_id)
        
    if not format_template:
        return await message.reply_text("ʏᴏ , ʏᴏᴜ ꜱᴇᴇᴍ ᴛᴏ ᴍɪꜱꜱ ꜱᴏᴍᴇᴛʜɪɴɢ, ᴄʜᴄᴇᴋ ʏᴏᴜʀ /ꜰᴏʀᴍᴀᴛ ᴀɢᴀɪɴ 😮‍💨")
     
    if user_id in user_file_counts:
        user_file_counts[user_id] += 1
        if user_file_counts[user_id] > file_count_limit:
            await message.reply_text(f"You have reached the file limit. Please wait for {sleep_duration // 300} minutes before sending more files.")
            await asyncio.sleep(sleep_duration)
            user_file_counts[user_id] = 0
    else:
        user_file_counts[user_id] = 1
        
    format_template = await db.get_format_template(user_id)
    media_preference = await db.get_media_preference(user_id)

    if not format_template:
        return await message.reply_text("ᴘʟᴇᴀsᴇ sᴇᴛ ᴀɴ ᴀᴜᴛᴏʀᴇɴᴀᴍᴇ ғᴏʀᴍᴀᴛ /format")

    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name
        media_type = media_preference or "document"
    elif message.video:
        file_id = message.video.file_id
        file_name = f"{message.video.file_name}.mp4"
        media_type = media_preference or "video"
    elif message.audio:
        file_id = message.audio.file_id
        file_name = f"{message.audio.file_name}.mp3"
        media_type = media_preference or "audio"
    else:
        return await message.reply_text("Unsupported file type")

    print(f"Original File Name: {file_name}")
    
    if file_id in renaming_operations:
        elapsed_time = (datetime.now() - renaming_operations[file_id]).seconds
        if elapsed_time < 10:
            print("File is being ignored as it is currently being renamed or was renamed recently.")
            return

    renaming_operations[file_id] = datetime.now()

    episode_number = extract_episode_number(file_name)

    print(f"Extracted Episode Number: {episode_number}")

    if episode_number:
        placeholders = ["episode", "Episode", "EPISODE", "{episode}"]
        for placeholder in placeholders:
            format_template = format_template.replace(placeholder, str(episode_number), 1)

        quality_placeholders = ["quality", "Quality", "QUALITY", "{quality}"]
        for quality_placeholder in quality_placeholders:
            if quality_placeholder in format_template:
                extracted_qualities = extract_quality(file_name)
                if extracted_qualities == "Unknown":
                    await message.reply_text("I wasn't able to extract the quality properly. Renaming as 'Unknown'...")
                    del renaming_operations[file_id]
                    return

                format_template = format_template.replace(quality_placeholder, "".join(extracted_qualities))

        _, file_extension = os.path.splitext(file_name)
        new_file_name = f"{format_template}"
        file_path = f"downloads/{new_file_name}"
        file = message

        download_msg = await message.reply_text(text="ᴛʀʏɪɴɢ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ...")
        try:
            path = await client.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=("ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ....", download_msg, time.time()))
        except Exception as e:
            del renaming_operations[file_id]
            return await download_msg.edit(e)
                _bool_metadata = await db.get_metadata(update.message.chat.id)

    if (_bool_metadata):
        metadata_path = f"Metadata/{new_filename}"
        metadata = await db.get_metadata_code(update.message.chat.id)
        if metadata:

            await ms.edit("I Fᴏᴜɴᴅ Yᴏᴜʀ Mᴇᴛᴀᴅᴀᴛᴀ\n\n__**Pʟᴇᴀsᴇ Wᴀɪᴛ...**__\n**Aᴅᴅɪɴɢ Mᴇᴛᴀᴅᴀᴛᴀ Tᴏ Fɪʟᴇ....**")
            cmd = f"""ffmpeg -i "{path}" {metadata} "{metadata_path}" """

            process = await asyncio.create_subprocess_shell(
                cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()
            er = stderr.decode()

            try:
                if er:
                    return await ms.edit(str(er) + "\n\n**Error**")
            except BaseException:
                pass
        await ms.edit("**Metadata added to the file successfully ✅**\n\n⚠️ __**Please wait...**__\n\n**Tʀyɪɴɢ Tᴏ Uᴩʟᴏᴀᴅɪɴɢ....**")
            
        duration = 0
        try:
            metadata = extractMetadata(createParser(file_path))
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
        except Exception as e:
            print(f"Error getting duration: {e}")

        upload_msg = await download_msg.edit("ᴛʀʏɪɴɢ ᴛᴏ ᴜᴘʟᴏᴀᴅɪɴɢ....")
        
        ph_path = None
        c_caption = await db.get_caption(message.chat.id)
        c_thumb = await db.get_thumbnail(message.chat.id)

        caption = c_caption.format(filename=new_file_name, filesize=humanbytes(message.document.file_size), duration=convert(duration)) if c_caption else f"**{new_file_name}**"

        if c_thumb:
            ph_path = await client.download_media(c_thumb)
            print(f"Thumbnail downloaded successfully. Path: {ph_path}")
        elif media_type == "video" and message.video.thumbs:
            ph_path = await client.download_media(message.video.thumbs[0].file_id)

        if ph_path:
            Image.open(ph_path).convert("RGB").save(ph_path)
            img = Image.open(ph_path)
            img.resize((320, 320))
            img.save(ph_path, "JPEG") 

        
        try:
            type = media_type
            if type == "document":
                await client.send_document(
                    message.chat.id,
                    document=metadata_path if _bool_metadata else file_path,
                    thumb=ph_path,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=("ᴜᴘʟᴏᴀᴅɪɴɢ....", upload_msg, time.time())
                )
            elif type == "video":
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InputMediaDocument, Message 
from PIL import Image
from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.utils import progress_for_pyrogram, humanbytes, convert
from helper.database import db
from helper.admins import is_admin
from config import Config
import os
import time
import re
import asyncio

# Initialize variables and directories
renaming_operations = {}
file_count_limit = 100
sleep_duration = 20 * 60 

if not os.path.isdir("Metadata"):
    os.mkdir("Metadata")
    
user_file_counts = {}

# Regular expressions for file name parsing
pattern1 = re.compile(r'S(\d+)(?:E|EP)(\d+)')
pattern2 = re.compile(r'S(\d+)\s*(?:E|EP|-\s*EP)(\d+)')
pattern3 = re.compile(r'(?:[([<{]?\s*(?:E|EP)\s*(\d+)\s*[)\]>}]?)')
pattern3_2 = re.compile(r'(?:\s*-\s*(\d+)\s*)')
pattern4 = re.compile(r'S(\d+)[^\d]*(\d+)', re.IGNORECASE)
patternX = re.compile(r'(\d+)')
pattern5 = re.compile(r'\b(?:.*?(\d{3,4}[^\dp]*p).*?|.*?(\d{3,4}p))\b', re.IGNORECASE)
pattern6 = re.compile(r'[([<{]?\s*4k\s*[)\]>}]?', re.IGNORECASE)
pattern7 = re.compile(r'[([<{]?\s*2k\s*[)\]>}]?', re.IGNORECASE)
pattern8 = re.compile(r'[([<{]?\s*HdRip\s*[)\]>}]?|\bHdRip\b', re.IGNORECASE)
pattern9 = re.compile(r'[([<{]?\s*4kX264\s*[)\]>}]?', re.IGNORECASE)
pattern10 = re.compile(r'[([<{]?\s*4kx265\s*[)\]>}]?', re.IGNORECASE)

# Function to extract quality from filename
def extract_quality(filename):
    match5 = re.search(pattern5, filename)
    if match5:
        quality5 = match5.group(1) or match5.group(2)
        return quality5

    match6 = re.search(pattern6, filename)
    if match6:
        return "4k"

    match7 = re.search(pattern7, filename)
    if match7:
        return "2k"

    match8 = re.search(pattern8, filename)
    if match8:
        return "HdRip"

    match9 = re.search(pattern9, filename)
    if match9:
        return "4kX264"

    match10 = re.search(pattern10, filename)
    if match10:
        return "4kx265"

    return "Unknown"

# Function to extract episode number from filename
def extract_episode_number(filename):    
    match = re.search(pattern1, filename)
    if match:
        return match.group(2)

    match = re.search(pattern2, filename)
    if match:
        return match.group(2)

    match = re.search(pattern3, filename)
    if match:
        return match.group(1)

    match = re.search(pattern3_2, filename)
    if match:
        return match.group(1)

    match = re.search(pattern4, filename)
    if match:
        return match.group(2)

    match = re.search(patternX, filename)
    if match:
        return match.group(1)

    return None

# Handle /format command to set renaming format
@Client.on_message(filters.private & filters.command("format"))
async def auto_rename_command(client, message):
    user_id = message.from_user.id
    format_template = message.text.split("/format", 1)[1].strip()
    await db.set_format_template(user_id, format_template)
    await message.reply_text("Rename format updated successfully!")

# Handle /setmedia command to set media preference
@Client.on_message(filters.private & filters.command("setmedia"))
async def set_media_command(client, message):
    user_id = message.from_user.id
    media_type = message.text.split("/setmedia", 1)[1].strip().lower()
    await db.set_media_preference(user_id, media_type)
    await message.reply_text(f"Media preference set to: {media_type}")

# Handle private messages with documents, videos, or audio files
@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def auto_rename_files(client, message):    
    user_id = message.from_user.id
    is_user_admin = await is_admin(user_id)
    if not is_user_admin and user_id not in Config.ADMIN:        
        await message.reply_text("You are not authorized to use me!")
        return    

    # Get user's format template and media preference
    format_template = await db.get_format_template(user_id)
    media_preference = await db.get_media_preference(user_id)
        
    if not format_template:
        return await message.reply_text("Please set an auto rename format using /format")

    # Limit file count per user
    if user_id in user_file_counts:
        user_file_counts[user_id] += 1
        if user_file_counts[user_id] > file_count_limit:
            await message.reply_text(f"You have reached the file limit. Please wait for {sleep_duration // 300} minutes before sending more files.")
            await asyncio.sleep(sleep_duration)
            user_file_counts[user_id] = 0
    else:
        user_file_counts[user_id] = 1
        
    # Determine media type and file name
    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name
        media_type = media_preference or "document"
    elif message.video:
        file_id = message.video.file_id
        file_name = f"{message.video.file_name}.mp4"
        media_type = media_preference or "video"
    elif message.audio:
        file_id = message.audio.file_id
        file_name = f"{message.audio.file_name}.mp3"
        media_type = media_preference or "audio"
    else:
        return await message.reply_text("Unsupported file type")

    # Print original file name and extract episode number
    print(f"Original File Name: {file_name}")
    episode_number = extract_episode_number(file_name)
    print(f"Extracted Episode Number: {episode_number}")

    # Process file renaming and metadata handling
    if episode_number:
        placeholders = ["episode", "Episode", "EPISODE", "{episode}"]
        for placeholder in placeholders:
            format_template = format_template.replace(placeholder, str(episode_number), 1)

        quality_placeholders = ["quality", "Quality", "QUALITY", "{quality}"]
        for quality_placeholder in quality_placeholders:
            if quality_placeholder in format_template:
                extracted_qualities = extract_quality(file_name)
                if extracted_qualities == "Unknown":
                    await message.reply_text("I wasn't able to extract the quality properly. Renaming as 'Unknown'...")
                    return

                format_template = format_template.replace(quality_placeholder, "".join(extracted_qualities))

        # Set new file name and path
        new_file_name = f"{format_template}"
        file_path = f"downloads/{new_file_name}"
        file = message

        # Download the file
        download_msg = await message.reply_text(text="Downloading...")
        try:
            path = await client.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=("Downloading...", download_msg, time.time()))
        except Exception as e:
            return await download_msg.edit(e)

        # Handle metadata if enabled
        bool_metadata = await db.get_metadata(user_id)
        if bool_metadata:
            metadata_path = f"Metadata/{new_file_name}"
            metadata = await db.get_metadata_code(user_id)
            if metadata:
                cmd = f"""ffmpeg -i "{path}" {metadata} "{metadata_path}" """

                process = await asyncio.create_subprocess_shell(
                    cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
                )

                stdout, stderr = await process.communicate()
                error = stderr.decode()

                if error:
                    return await download_msg.edit(str(error) + "\n\nError")

            await download_msg.edit("Metadata added to the file successfully ✅")

        # Get file duration for videos and audios
        duration = 0
        try:
            metadata = extractMetadata(createParser(file_path))
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
        except Exception as e:
            print(f"Error getting duration: {e}")

        # Send the file with appropriate media type
        upload_msg = await download_msg.edit("Uploading...")
        try:
            if media_type == "document":
                await client.send_document(
                    message.chat.id,
                    document=metadata_path if bool_metadata else file_path,
                    caption=new_file_name,
                    progress=progress_for_pyrogram,
                    progress_args=("Uploading...", upload_msg, time.time())
                )
            elif media_type == "video":
                await client.send_video(
                    message.chat.id,
                    document=metadata_path if bool_metadata else file_path,
                    caption=new_file_name,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("Uploading...", upload_msg, time.time())
                )
            elif media_type == "audio":
                await client.send_audio(
                    message.chat.id,
                    document=metadata_path if bool_metadata else file_path,
                    caption=new_file_name,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("Uploading...", upload_msg, time.time())
                )
        except Exception as e:
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            if metadata_path:
                os.remove(metadata_path)
            if path:
                os.remove(path)
            return await ms.edit(f" Eʀʀᴏʀ {e}")

    await download_msg.delete() 

    if ph_path:
        os.remove(ph_path)
    if file_path:
        os.remove(file_path)
    if metadata_path:
        os.remove(metadata_path)
        
        del renaming_operations[file_id]
