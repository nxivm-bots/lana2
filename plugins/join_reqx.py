from pyrogram import Client, filters, enums
#from pyrogram.types import ChatJoinRequest ,Message
from database.join_reqsx import JoinReqsx
from config import ADMINS, FORCE_SUB_CHANNEL3
from pyrogram.types import *

jishubotx = JoinReqsx




@Client.on_chat_join_request(filters.chat(FORCE_SUB_CHANNEL3 if FORCE_SUB_CHANNEL3 else "self"))
async def join_reqsx(client: Client, join_req: ChatJoinRequest):

    if jishubotx().isActive():
        user_id = join_req.from_user.id
        first_name = join_req.from_user.first_name
        username = join_req.from_user.username
        date = join_req.date

        await jishubotx().add_user(
            user_id=user_id,
            first_name=first_name,
            username=username,
            date=date
        )
