import re, os, time

id_pattern = re.compile(r'^.\d+$') 

class Config(object):
    # pyro client config
    API_ID    = os.environ.get("API_ID", "22418774")
    API_HASH  = os.environ.get("API_HASH", "d8c8dab274f9a811814a6a96d044028e")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "") 

    # database config
    DB_NAME = os.environ.get("DB_NAME","obi")     
    DB_URL  = os.environ.get("DB_URL","mongodb+srv://mehtadmphta33:Mehtab1234@cluster0.bfsb3oq.mongodb.net/?retryWrites=true&w=majority")
 
    # other configs
    BOT_UPTIME  = time.time()
    START_PIC   = os.environ.get("START_PIC", "https://graph.org/file/a39c43ccf6c454d30eaec.mp4")
    ADMIN       = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '6299128233').split()]
    FORCE_SUB   = os.environ.get("FORCE_SUB", "UchihaPoliceUpdates") 
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002008965715"))

    # wes response configuration     
    WEBHOOK = bool(os.environ.get("WEBHOOK", "True"))


class Txt(object):

    SEQUENCE_TXT = """ᴛʜᴇ ꜰɪʟᴇ sᴇQᴜᴇɴᴄɪɴɢ ʙᴏᴛ. ʜᴇʀᴇ's ʜᴏᴡ ᴛᴏ ᴜsᴇ:

1. Usᴇ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ /startsequence ᴛᴏ ʙᴇɢɪɴ ᴀ ꜰɪʟᴇ sᴇQᴜᴇɴᴄɪɴɢ ᴘʀᴏᴄᴇss.
2. Sᴇɴᴅ ᴛʜᴇ ꜰɪʟᴇs ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴇQᴜᴇɴᴄᴇ ᴏɴᴇ ʙʏ ᴏɴᴇ.
3. Wʜᴇɴ ʏᴏᴜ'ʀᴇ ᴅᴏɴᴇ, Usᴇ /endsequence ᴛᴏ ꜰɪɴɪsʜ ᴀɴᴅ ɢᴇᴛ ᴛʜᴇ sᴇQᴜᴇɴᴄᴇᴅ ꜰɪʟᴇs.

SᴇQᴜᴇɴᴄᴇ Bᴏᴛ: @RinNohara_xBot
    
    """
        
    START_TXT = """Hᴇʟʟᴏ {}
I'ᴍ **Oʙɪᴛᴏ Uᴄʜɪʜᴀ**, ᴀɴ ᴀᴜᴛᴏʀᴇɴᴀᴍᴇ ʙᴏᴛ ᴛʜᴀᴛ ʀᴇɴᴀᴍᴇs ᴀɴɪᴍᴇ ғɪʟᴇs ᴛᴏ ᴛʜᴇ ғᴏʀᴍᴀᴛ ʏᴏᴜ sᴇᴛ."
Tᴏ sᴇᴇ ᴍʏ ғᴜɴᴄᴛɪᴏɴs, ᴜsᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ."""
    
    FILE_NAME_TXT = """
    <u><b>SETUP AUTO RENAME FORMAT</b></u>\n\nUse These Keywords To Setup Custom File Name\n\n➝ episode :- to replace episode number\n➝ quality :- to replace video resolution\n\n‣ <b>Example :</b> /autorename [AL] High Card S1 - Eepisode [quality] Sub @Anime_Locus.mkv\n\n‣ <b>Your Current Rename Format :</b> {format_template}
    """
    
    ABOUT_TXT = f"""<b>╭───────────⍟
├🤖 My name: <a href=http://t.me/UchihaObito_xBot>Uᴄʜɪʜᴀ Oʙɪᴛᴏ</a>
├📕 Library: <a href=https://github.com/pyrogram>Pyʀᴏɢʀᴀᴍ</a>
├✏️ Language: <a href=https://www.python.org>Pyᴛʜᴏɴ3</a>
├💾 Data Base: <a href=https://cloud.mongodb.com>Mᴏɴɢᴏ DB</a>
├📊 Build Version: `OBI V1.7.0`
├🔗 GitHub: <a href=https://github.com/illuminati-Dev>GitHub</a>
├📧 Contact: <a href=https://telegram.me/The_NanamiiKento>N A N A M I</a>
╰───────────────⍟ 
"""

    
    THUMB_TXT = """ • /start the bot and send any photo to automatically set the thumbnail.
• /del_thumb to delete your old thumbnail.
• /view_thumb to view your current thumbnail."""

    PREMIUM_TXT = """Hm Soon
    for now free use kr lo"""

#⚠️ Dᴏɴ'ᴛ Rᴇᴍᴏᴠᴇ Oᴜʀ Cʀᴇᴅɪᴛꜱ @ᴩyʀᴏ_ʙᴏᴛᴢ🙏🥲
    COMMANDS_TXT = """🌌 How To Set Thumbnail
  
• /start the bot and send any photo to automatically set the thumbnail.
• /del_thumb to delete your old thumbnail.
• /view_thumb to view your current thumbnail.

📑 How To Set Custom Caption
• /set_caption - Use this command to set a custom caption.
• /see_caption - Use this command to view your custom caption.
• /del_caption - Use this command to delete your custom caption.
Example: /set_caption 📕 File Name: {filename}
💾 Size: {filesize}
⏰ Duration: {duration}

✏️ How To Rename A File
• Send any file and type the new file name and select the format [document, video, audio].    """

    PROGRESS_BAR = """<b>\n
╭━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱━➣
┣⪼ 🗃️ Sɪᴢᴇ: {1} | {2}
┣⪼ ⏳️ Dᴏɴᴇ : {0}%
┣⪼ 🚀 Sᴩᴇᴇᴅ: {3}/s
┣⪼ ⏰️ Eᴛᴀ: {4}
╰━━━━━━━━━━━━━━━➣ </b>"""


