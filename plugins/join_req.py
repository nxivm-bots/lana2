from pyrogram import Client, filters, enums
#from pyrogram.types import ChatJoinRequest ,Message
from database.join_reqs import JoinReqs
from config import ADMINS, FORCE_SUB_CHANNEL
from pyrogram.types import *

jishubotz = JoinReqs




@Client.on_chat_join_request(filters.chat(FORCE_SUB_CHANNEL if FORCE_SUB_CHANNEL else "self"))
async def join_reqs(client: Client, join_req: ChatJoinRequest):

    if jishubotz().isActive():
        user_id = join_req.from_user.id
        first_name = join_req.from_user.first_name
        username = join_req.from_user.username
        date = join_req.date

        await jishubotz().add_user(
            user_id=user_id,
            first_name=first_name,
            username=username,
            date=date
        )
"""
@Client.on_message(filters.command("total") & filters.private & filters.user(ADMINS))
async def total_requests(client: Client, message: Message):

    if jishubotz().isActive():
        total = await jishubotz().get_all_users_count()
        await message.reply_text(
            text=f"**🗿 Total Requests :** `{total}`",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            quote=True)


@Client.on_message(filters.command("clear") & filters.private & filters.user(ADMINS))
async def purge_requests(client: Client, message: Message):
    
    if jishubotz().isActive():
        await jishubotz().delete_all_users()
        await message.reply_text(
            text="Cleared All Requests 🧹",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            quote=True)

"""


        
