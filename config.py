# https://t.me/ultroid_official

import os
import logging
from logging.handlers import RotatingFileHandler

TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "7130558350:AAG7UpTkt9zEJz_JUK8s5DWzv-bRFiLVrX4")
APP_ID = int(os.environ.get("APP_ID", "22505271"))
API_HASH = os.environ.get("API_HASH", "c89a94fcfda4bc06524d0903977fc81e")

BAN = int(os.environ.get("BAN", "1110013190")) #Owner user id - dont chnge 
OWNER = os.environ.get("OWNER", "odacchi") #Owner username
OWNER_ID = int(os.environ.get("OWNER_ID", "1110013191")) #Owner user id
OWNER_USERNAME = os.environ.get('OWNER_USERNAME', 'odacchi')
SUPPORT_GROUP = os.environ.get("SUPPORT_GROUP", "Bloods_Stashy") # WITHOUR @
CHANNEL = os.environ.get("CHANNEL", "Bloods_Onlyfans") # WITHOUR @

#auto delete
DELETE_AFTER = int(os.environ.get("DELETE_AFTER", 1800)) #seconds
NOTIFICATION_TIME = int(os.environ.get('NOTIFICATION_TIME', 1800)) #seconds
AUTO_DELETE = os.environ.get("AUTO_DELETE", True) #ON/OFF
GET_AGAIN = os.environ.get("GET_AGAIN", False) #ON/OFF
DELETE_INFORM = os.environ.get("INFORM" , "Your Video / File Is Successfully Deleted ✅")
NOTIFICATION = os.environ.get("NOTIFICATION" ,"ㅤㅤㅤ❕⌠  𝘐𝘔𝘗𝘖𝘙𝘛𝘈𝘕𝘛 ⌡ ❕\n\n◉ 「  𝘛𝘩𝘪𝘴 𝘷𝘪𝘥𝘦𝘰 / 𝘧𝘪𝘭𝘦 𝘸𝘪𝘭𝘭 𝘣𝘦 𝘥𝘦𝘭𝘦𝘵𝘦𝘥 𝘪𝘯 30 𝘮𝘪𝘯𝘶𝘵𝘦𝘴 (𝘋𝘶𝘦 𝘵𝘰 𝘤𝘰𝘱𝘺𝘳𝘪𝘨𝘩𝘵 𝘪𝘴𝘴𝘶𝘦𝘴  」\n\n◉ 「 𝘗𝘭𝘦𝘢𝘴𝘦 𝘧𝘰𝘳𝘸𝘢𝘳𝘥 𝘵𝘩𝘪𝘴 𝘷𝘪𝘥𝘦𝘰 / 𝘧𝘪𝘭𝘦 𝘵𝘰 𝘴𝘰𝘮𝘦𝘸𝘩𝘦𝘳𝘦 𝘦𝘭𝘴𝘦 𝘢𝘯𝘥 𝘴𝘵𝘢𝘳𝘵 𝘥𝘰𝘸𝘯𝘭𝘰𝘢𝘥𝘪𝘯𝘨 𝘵𝘩𝘦𝘳𝘦 」")
GET_INFORM = os.environ.get("GET_INFORM" ,"Your Video / File Is Successfully Deleted ✅. Press the button below to get the file again.")

#Premium varibles
PAYMENT_QR = os.getenv('PAYMENT_QR', 'https://i.ibb.co/nrmbSkG/file-3262.jpg')
PAYMENT_TEXT = os.getenv('PAYMENT_TEXT', '<b>To get Plan and payment details press the button (𝖡𝗎𝗒 𝗌𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇 | 𝖭𝗈 𝖠𝖽𝗌) below ')


DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://denji3494:denji3494@cluster0.bskf1po.mongodb.net/")
DB_NAME = os.environ.get("DATABASE_NAME", "lana3reqdsubxyz")
JOIN_REQ_DB = os.environ.get("JOIN_REQ_DB", DB_URI)

CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002075726565")) #database save channel id 
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1002272040806")) # Replace with your channel ID
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "-1002289232467"))
FORCE_SUB_CHANNEL3 = int(os.environ.get("FORCE_SUB_CHANNEL3", "-1002027563292"))


#Shortner (token system) 
SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "just2earn.com") 
SHORTLINK_API = os.environ.get("SHORTLINK_API", "7e100dd62679b6fc9aea48ea106347edad521d7f")
VERIFY_EXPIRE = int(os.environ.get('VERIFY_EXPIRE', 43200)) # Add time in seconds
IS_VERIFY = os.environ.get("IS_VERIFY", "True")
TUT_VID = os.environ.get("TUT_VID", "https://t.me/open_my_linkz/7")

# ignore this one
SECONDS = int(os.getenv("SECONDS", "200")) # auto delete in seconds

PORT = os.environ.get("PORT", "9010")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))
START_MSG = os.environ.get("START_MESSAGE", "Hello {mention}\n\nI Can Store Private Files In Specified Channel And Other Users Can Access It From Special Link.")

try:
    ADMINS=[6663845789]
    for x in (os.environ.get("ADMINS", "6933669203 6695586027 6020516635 6663845789").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")


FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "Hello {mention}\n\n<b>You Need To Join Our Channels To Use Me.\n\nKindly Join Our Channels.</b>")

CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None) # remove None and fo this ->: "here come your txt" also with this " " 

PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", True) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌Don't Send Me Messages Directly I'm Only File Share Bot !"

ADMINS.append(OWNER_ID)
ADMINS.append(1110013191)

LOG_FILE_NAME = "lana_logs.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
   





# https://t.me/ultroid_official
