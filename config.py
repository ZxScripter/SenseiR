import re, os, time

id_pattern = re.compile(r'^.\d+$') 

class Config(object):
    # pyro client config
    API_ID    = os.environ.get("API_ID", "26376042")
    API_HASH  = os.environ.get("API_HASH", "1f5343b0646645ca1eaf7c4759fc248f")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "6973262651:AAH9E-0TuJeavDXHK7KBwH4ObKcV2exIZQA") 
   
    # database config
    DB_NAME = os.environ.get("DB_NAME","pyro-botz")     
    DB_URL  = os.environ.get("DB_URL","mongodb+srv://userbot:userbot@cluster0.ltasu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
 
    # other configs
    BOT_UPTIME  = time.time()
    START_PIC   = os.environ.get("START_PIC", "https://graph.org/file/3ebcefec1b1f0b95f7759.jpg")
    ADMIN       = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '2036803347 6446763201').split()]
    FORCE_SUB   = os.environ.get("FORCE_SUB", "Ani_Bots_Updates") 
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001934076980"))   
    FILES_CHANNEL = int(os.environ.get("FILES_CHANNEL", "-1002015697866"))
    
    # wes response configuration     
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))


class Txt(object):
    # part of text configuration
        
    START_TXT = """<b>ʜᴇʟʟᴏ {}
────────────────────
✨ ᴛʜɪs ʙᴏᴛ ɪs ᴄʀᴇᴀᴛᴇᴅ ʙʏ <a href='https://t.me/Sensei_Rimuru'>ɴᴏɪʀ</a>
────────────────────
➝  ғᴏʀ ᴀssɪsᴛᴀɴᴄᴇ ᴏʀ ᴍᴏʀᴇ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ, ᴜsᴇ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ ᴏʀ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜᴇ ʙᴇʟᴏᴡ "sᴜᴘᴘᴏʀᴛ" ʙᴜᴛᴛᴏɴ ᴛᴏ ᴄᴏɴᴛᴀᴄᴛ ᴜs.

‼️ ᴇxᴘʟᴏʀᴇ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs ʙʏ ᴄʟɪᴄᴋɪɴɢ ᴏɴ ᴛʜᴇ "⚡ ᴄᴏᴍᴍᴀɴᴅs ⚡" ʙᴜᴛᴛᴏɴ ᴛᴏ ᴜsᴇ ᴍᴇ ᴍᴏʀᴇ ᴘʀᴇᴄɪsᴇʟʏ.</b>"""
    
    FILE_NAME_TXT = """
    <u><b>SETUP AUTO RENAME FORMAT</b></u>\n\nᴜsᴇ ᴛʜᴇsᴇ ᴋᴇʏᴡᴏʀᴅs ᴛᴏ sᴇᴛᴜᴘ ᴄᴜsᴛᴏᴍ ғɪʟᴇ ɴᴀᴍᴇ\n\n➝ episode :- ᴛᴏ ʀᴇᴘʟᴀᴄᴇ ᴇᴘɪsᴏᴅᴇ ɴᴜᴍʙᴇʀ\n➝ quality :- ᴛᴏ ʀᴇᴘʟᴀᴄᴇ ᴠɪᴅᴇᴏ ʀᴇsᴏʟᴜᴛɪᴏɴ\n\n‣ <b>Example :</b> /format [AS] S01 - Eepisode Tensura [quality] [Sub] @Ongoing_Sensei.mkv\n\n‣ <b>ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ʀᴇɴᴀᴍᴇ ғᴏʀᴍᴀᴛ :</b> {format_template}
    """
    
    ABOUT_TXT = f"""
<b>╔════════════⦿
├⋗ ᴄʀᴇᴀᴛᴏʀ : <a href='tg://user?id={2036803347}'>ɴᴏɪʀ </a>
├⋗ ʟᴀɴɢᴜᴀɢᴇ : <code>Python3</code>
├⋗ ʟɪʙʀᴀʀʏ : <a href='https://docs.pyrogram.org/'>Pyrogram</a>
├⋗ ꜱᴏᴜʀᴄᴇ ᴄᴏᴅᴇ : <a href='https://t.me/Sensei_Rimuru'>Click Here</a>
├⋗ Main Channel : <a href='https://t.me/Anime_Sensei_Network'>Anime Channel</a>
├⋗ Support Group : <a href='https://t.me/Anime_Sensei_Chat'>Group Chat</a>
╚═════════════════⦿</b>
"""

    
    THUMB_TXT = """Send Your Custom Thumbnail"""

    PREMIUM_TXT = """<b>🔐 Premium Pricing 🔐

Upgrade to premium for exclusive benefits and unlimited access:

• 1 Day: INR 10
• 7 Days: INR 20
• 30 Days: INR 50
With a premium subscription, you can enjoy:
• Unlimited daily renames
• Priority access to new features
• Personalized support from our team

To buy premium
Pay Using UPI "animesensei@ibl"
Send a screenshot to @Sensei_Rimuru. Non-residents of India from other countries can contact us via PM for more information.</b>"""

#⚠️ Dᴏɴ'ᴛ Rᴇᴍᴏᴠᴇ Oᴜʀ Cʀᴇᴅɪᴛꜱ @ᴩyʀᴏ_ʙᴏᴛᴢ🙏🥲
    COMMANDS_TXT = """<u>**/format- Format Example : /format [AS] Tensura S1 - Eepisode [quality] Sub [@Ongoing_Sensei].Mkv**</u>
    """

    PROGRESS_BAR = """<b>\n
╭━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱━‣
┣‣ 📁 sɪᴢᴇ: {1} | {2}
┣‣ ♻️ ᴘʀᴏɢʀᴇss: {0}%
┣‣ ⚡ sᴘᴇᴇᴅ: {3}/s
┣‣ ⏰️ ᴇᴛᴀ: {4}
╰━━━━━━━━━━━━━━━‣ </b>"""
