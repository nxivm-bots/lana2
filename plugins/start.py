# line number 160-169 check for changes - token
from pymongo import MongoClient
import asyncio
import base64
import logging
import os
import random
import re
import string
import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import *
from helper_func import *
from database.database import *
from shortzy import Shortzy

#delete_after = 600

client = MongoClient(DB_URI)  # Replace with your MongoDB URI
db = client[DB_NAME]  # Database name
phdlust = db["phdlust"]  # Collection for users
phdlust_tasks = db["phdlust_tasks"] 

# MongoDB Helper Functions
async def add_premium_user(user_id, duration_in_days):
    expiry_time = time.time() + (duration_in_days * 86400)  # Calculate expiry time in seconds
    phdlust.update_one(
        {"user_id": user_id},
        {"$set": {"is_premium": True, "expiry_time": expiry_time}},
        upsert=True
    )

async def remove_premium_user(user_id):
    phdlust.update_one(
        {"user_id": user_id},
        {"$set": {"is_premium": False, "expiry_time": None}}
    )

async def get_user_subscription(user_id):
    user = phdlust.find_one({"user_id": user_id})
    if user:
        return user.get("is_premium", False), user.get("expiry_time", None)
    return False, None

async def is_premium_user(user_id):
    is_premium, expiry_time = await get_user_subscription(user_id)
    if is_premium and expiry_time > time.time():
        return True
    return False

'''
#async def is_subscribed(client, update):
async def is_subscribed(filter, client, update):
    user_id = update.from_user.id

    # Admins bypass subscription checks
    if user_id in ADMINS:
        return True

    # Normal force subscription check
    force_sub_channels = await get_force_sub_channels()
    member_status = {ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER}

    for channel_id in force_sub_channels:
        try:
            member = await client.get_chat_member(chat_id=channel_id, user_id=user_id)
            if member.status not in member_status:
                return False
        except UserNotParticipant:
            return False

    # Request join check (using FORCE_SUB_CHANNEL from config.py)
    
    if not FORCE_SUB_CHANNEL:
        return True

    if not FORCE_SUB_CHANNEL2:
        return True

    if not FORCE_SUB_CHANNEL3:
        return True

    if FORCE_SUB_CHANNEL:
        
        user_id = update.from_user.id
        user = await jishubotz().get_user(update.from_user.id)
        
        if user_id in ADMINS:
            return True
        
        if user and user["user_id"] == update.from_user.id:
            return True  
        
        try:
            member = await client.get_chat_member(chat_id = FORCE_SUB_CHANNEL, user_id = user_id)
        except UserNotParticipant:
            return False
    
        if not member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
            return False
        else:
            return True
            
    if FORCE_SUB_CHANNEL2:
        
        user_id = update.from_user.id
        user = await jishuboty().get_user(update.from_user.id)
        
        if user_id in ADMINS:
            return True
        
        if user and user["user_id"] == update.from_user.id:
            return True  
        
        try:
            member = await client.get_chat_member(chat_id = FORCE_SUB_CHANNEL2, user_id = user_id)
        except UserNotParticipant:
            return False
    
        if not member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
            return False
        else:
            return True

    if FORCE_SUB_CHANNEL3:
        
        user_id = update.from_user.id
        user = await jishubotx().get_user(update.from_user.id)
        
        if user_id in ADMINS:
            return True
        
        if user and user["user_id"] == update.from_user.id:
            return True  
        
        try:
            member = await client.get_chat_member(chat_id = FORCE_SUB_CHANNEL3, user_id = user_id)
        except UserNotParticipant:
            return False
    
        if not member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
            return False
        else:
            return True
'''

# Function to add a delete task to the database
async def add_delete_task(chat_id, message_id, delete_at):
    phdlust_tasks.insert_one({
        "chat_id": chat_id,
        "message_id": message_id,
        "delete_at": delete_at
    })

# Function to delete the notification after a set delay
async def delete_notification(client, chat_id, notification_id, delay):
    await asyncio.sleep(delay)
    try:
        # Delete the notification message
        await client.delete_messages(chat_id=chat_id, message_ids=notification_id)
    except Exception as e:
        print(f"Error deleting notification {notification_id} in chat {chat_id}: {e}")
        
async def schedule_auto_delete(client, chat_id, message_id, delay):
    delete_at = datetime.now() + timedelta(seconds=int(delay))
    await add_delete_task(chat_id, message_id, delete_at)
    
    # Run deletion in the background to prevent blocking
    async def delete_message():
        await asyncio.sleep(int(delay))
        try:
            # Delete the original message
            await client.delete_messages(chat_id=chat_id, message_ids=message_id)
            phdlust_tasks.delete_one({"chat_id": chat_id, "message_id": message_id})  # Remove from DB
            
            # Send a notification about the deletion
            notification_text = DELETE_INFORM
            notification_msg = await client.send_message(chat_id, notification_text)
            
            # Schedule deletion of the notification after 60 seconds
            asyncio.create_task(delete_notification(client, chat_id, notification_msg.id, 40))
        
        except Exception as e:
            print(f"Error deleting message {message_id} in chat {chat_id}: {e}")

    asyncio.create_task(delete_message())  


async def delete_notification_after_delay(client, chat_id, message_id, delay):
    await asyncio.sleep(delay)
    try:
        # Delete the notification message
        await client.delete_messages(chat_id=chat_id, message_ids=message_id)
    except Exception as e:
        print(f"Error deleting notification {message_id} in chat {chat_id}: {e}")
        
        
@Bot.on_message(filters.command('start') & filters.private & subscribed )
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    UBAN = BAN  # Fetch the owner's ID from config
    
    # Schedule the initial message for deletion after 10 minutes
    #await schedule_auto_delete(client, message.chat.id, message.id, delay=600)

    # Check if the user is the owner
    if id == UBAN:
        sent_message = await message.reply("You are the U-BAN! Additional actions can be added here.")
    else:
        if not await present_user(id):
            try:
                await add_user(id)
            except Exception as e:
                print(f"Error adding user: {e}")

        premium_status = await is_premium_user(id)
        verify_status = await get_verify_status(id)

        # Check verification status
        if verify_status['is_verified'] and VERIFY_EXPIRE < (time.time() - verify_status['verified_time']):
            await update_verify_status(id, is_verified=False)

        # Handle token verification link
        if "verify_" in message.text:
            _, token = message.text.split("_", 1)
            if verify_status['verify_token'] != token:
                sent_message = await message.reply("Your token is invalid or expired. Try again by clicking /start.")
                return
            await update_verify_status(id, is_verified=True, verified_time=time.time())
            sent_message = await message.reply("Your token was successfully verified and is valid for 1 Hour.")
        elif len(message.text) > 7 and (verify_status['is_verified'] or premium_status):
            try:
                base64_string = message.text.split(" ", 1)[1]
            except:
                return
            _string = await decode(base64_string)
            argument = _string.split("-")
            ids = []

            if len(argument) == 3:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = range(start, end+1) if start <= end else []
            elif len(argument) == 2:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]

            temp_msg = await message.reply("Please wait...")

            try:
                messages = await get_messages(client, ids)
            except:
                error_msg = await message.reply_text("Something went wrong..!")
                return
            await temp_msg.delete()

            phdlusts = []
            messages = await get_messages(client, ids)
            for msg in messages:
                if bool(CUSTOM_CAPTION) & bool(msg.document):
                    caption = CUSTOM_CAPTION.format(previouscaption = "" if not msg.caption else msg.caption.html, filename = msg.document.file_name)
                else:
                    caption = "" if not msg.caption else msg.caption.html

                if DISABLE_CHANNEL_BUTTON:
                    reply_markup = msg.reply_markup
                else:
                    reply_markup = None
                
                try:
                    messages = await get_messages(client, ids)
                    phdlust = await msg.copy(chat_id=message.from_user.id, caption=caption, reply_markup=reply_markup , protect_content=PROTECT_CONTENT)
                    phdlusts.append(phdlust)
                    if AUTO_DELETE == True:
                        #await message.reply_text(f"The message will be automatically deleted in {delete_after} seconds.")
                        asyncio.create_task(schedule_auto_delete(client, phdlust.chat.id, phdlust.id, delay=DELETE_AFTER))
                    await asyncio.sleep(0.2)      
                    #asyncio.sleep(0.2)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    phdlust = await msg.copy(chat_id=message.from_user.id, caption=caption, reply_markup=reply_markup , protect_content=PROTECT_CONTENT)
                    phdlusts.append(phdlust)     

            # Notify user to get file again if messages are auto-deleted
            if GET_AGAIN == True:
                get_file_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton("GET FILE AGAIN", url=f"https://t.me/{client.username}?start={message.text.split()[1]}")]
                ])
                await message.reply(GET_INFORM, reply_markup=get_file_markup)

            if AUTO_DELETE == True:
                delete_notification = await message.reply(NOTIFICATION)
                asyncio.create_task(delete_notification_after_delay(client, delete_notification.chat.id, delete_notification.id, delay=NOTIFICATION_TIME))
              
        elif verify_status['is_verified'] or premium_status:
            reply_markup = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Premium", callback_data="premium"), InlineKeyboardButton("Close", callback_data="close")]
                ]
            )
            welcome_message = await message.reply_text(
                text=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=None if not message.from_user.username else '@' + message.from_user.username,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                quote=True
            )
        else:
            verify_status = await get_verify_status(id)
            if IS_VERIFY and not verify_status['is_verified']:
                token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                await update_verify_status(id, verify_token=token, link="")
                link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, f'https://telegram.dog/{client.username}?start=verify_{token}')
                buttons = [
                    [InlineKeyboardButton("￫ 𝖵𝖾𝗋𝗂𝖿𝗒", url=link), InlineKeyboardButton("￫ 𝖳𝗎𝗍𝗈𝗋𝗂𝖺𝗅", url=TUT_VID)],
                    [InlineKeyboardButton("𝖡𝗎𝗒 𝗌𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇 | 𝖭𝗈 𝖠𝖽𝗌", callback_data="premium")]
                ]
                verification_message = await message.reply(
                    f"Your Ads token is expired, refresh your token and try again.\n\nToken Timeout: {get_exp_time(VERIFY_EXPIRE)}\n\nWhat is the token?\n\nThis is an ads token. If you pass 1 ad, you can use the bot for {get_exp_time(VERIFY_EXPIRE)} after passing the ad.",
                    reply_markup=InlineKeyboardMarkup(buttons),
                    protect_content=PROTECT_CONTENT,
                    quote=True
                )
                #await schedule_auto_delete(client, verification_message.chat.id, verification_message.id, delay=600)



    
#=====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""

FORCE_MSG = """╭𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖲𝗍𝖺𝗍𝗎𝗌 :

{status_list}

𝖧𝖾𝗒 {mention}, 𝖯𝗅𝖾𝖺𝗌𝖾 𝖩𝗈𝗂𝗇 𝗆𝗒 𝖢𝗁𝖺𝗇𝗇𝖾𝗅𝗌 𝖺𝗇𝖽 𝗍𝗁𝖾𝗇 𝖼𝗅𝗂𝖼𝗄 𝗈𝗇 '↺𝖱𝖾𝖿𝗋𝖾𝗌h' 𝗍𝗈 𝗀𝖾𝗍 𝗒𝗈𝗎𝗋 𝖤𝗉𝗂𝗌𝗈𝖽𝖾'𝗌"""

#=====================================================================================##
@Client.on_message(filters.command("start") & filters.private)
async def not_joined(client: Client, message: Message):
    user_id = message.from_user.id
    force_sub_channels = await get_force_sub_channels()
    status_list = []
    temp_buttons = []  # collect all buttons here first

    for i, channel_id in enumerate(force_sub_channels):
        try:
            invite_info = await channels_collection.find_one({"channel_id": channel_id})
            invite_link = invite_info.get("invite_link") if invite_info else None
            expires_at = invite_info.get("expires_at") if invite_info else None

            # Generate a new invite link if expired or not found
            if not invite_link or not expires_at or datetime.utcnow() > expires_at:
                new_invite_link = await client.export_chat_invite_link(channel_id)
                expires_in = timedelta(hours=1)
                expires_at = datetime.utcnow() + expires_in

                await channels_collection.update_one(
                    {"channel_id": channel_id},
                    {"$set": {"invite_link": new_invite_link, "expires_at": expires_at}},
                    upsert=True,
                )
                invite_link = new_invite_link
                
                # Notify admins about the link reset
                for admin_id in ADMINS:
                    try:
                        await client.send_message(
                            chat_id=admin_id,
                            text=f"<b>Invite link for channel {channel_id} has been reset.\nNew link: {new_invite_link}</b>",
                        )
                    except Exception as e:
                        print(f"Error notifying admin {admin_id}: {e}")

            # Check membership
            try:
                member = await client.get_chat_member(chat_id=channel_id, user_id=user_id)
                if member.status in {ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER}:
                    status_list.append(f"⭕️ Channel {i + 1} - ✅ 𝖩𝗈𝗂𝗇𝖾𝖽")
                else:
                    status_list.append(f"⭕️ Channel {i + 1} - ❌ 𝖭𝗈𝗍 𝖩𝗈𝗂𝗇𝖾𝖽")
                    temp_buttons.append(InlineKeyboardButton(f"Join Channel {i + 1}", url=invite_link))

            except UserNotParticipant:
                status_list.append(f"⭕️ Channel {i + 1} - ❌ 𝖭𝗈𝗍 𝖩𝗈𝗂𝗇𝖾𝖽")
                temp_buttons.append(InlineKeyboardButton(f"Join Channel {i + 1}", url=invite_link))
            except Exception as e:
                print(f"Error checking membership for {channel_id}: {e}")
                status_list.append(f"⭕️ Channel {i + 1} - ⚠️ Error")
                temp_buttons.append(InlineKeyboardButton(f"Join Channel {i + 1}", url=invite_link))

        except Exception as e:
            print(f"Error processing channel {channel_id}: {e}")
            status_list.append(f"⭕️ Channel {i + 1} - ⚠️ Error")
            temp_buttons.append(InlineKeyboardButton(f"Error < Help {i + 1}", url=f"https://t.me/{OWNER_USERNAME}"))

    # Check special FORCE_SUB_CHANNEL (pending join requests)
    # FORCE_SUB_CHANNEL 1
    if FORCE_SUB_CHANNEL:
        try:
            member = await client.get_chat_member(chat_id=FORCE_SUB_CHANNEL, user_id=user_id)
            if member.status in {ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER}:
                status_list.append("🔹 Channel 1 - ✅ Joined")
            else:
                raise UserNotParticipant
        except UserNotParticipant:
            user = await jishubotz().get_user(user_id)
            if user and user["user_id"] == user_id:
                status_list.append("🔹 Channel 1 - ✅ Requested")
            else:
                # check cached link from DB
                invite_info = await req_collection.find_one({"channel_id": FORCE_SUB_CHANNEL})
                invite_link = invite_info.get("invite_link") if invite_info else None
                expires_at = invite_info.get("expires_at") if invite_info else None
    
                if not invite_link or not expires_at or datetime.utcnow() > expires_at:
                    try:
                        expire_at = datetime.utcnow() + timedelta(hours=1)
                        join_request_link = await client.create_chat_invite_link(
                            chat_id=FORCE_SUB_CHANNEL,
                            creates_join_request=True,
                            expire_date=expire_at
                        )
                        invite_link = join_request_link.invite_link
                        await req_collection.update_one(
                            {"channel_id": FORCE_SUB_CHANNEL},
                            {"$set": {"invite_link": invite_link, "expires_at": expire_at}},
                            upsert=True
                        )
                        for admin_id in ADMINS:
                            try:
                                await client.send_message(
                                    chat_id=admin_id,
                                    text=f"<b>rInvite link for channel {FORCE_SUB_CHANNEL} has been reset.\nNew link: {invite_link}</b>",
                                    disable_web_page_preview=True
                                )
                            except Exception as e:
                                print(f"[Notify Admin Fallback Error] {admin_id}: {e}")
                    except Exception as e:
                        print(f"[JoinRequest1 Failed] {e}")
                        try:
                            invite_link = await client.export_chat_invite_link(FORCE_SUB_CHANNEL)
                        except Exception as e2:
                            print(f"[Export1 Failed] {e2}")
    
                status_list.append("🔹 Channel 1 - ❌ Not Joined")
                if invite_link:
                    temp_buttons.append(InlineKeyboardButton("Join Channel 1", url=invite_link))
                else:
                    status_list.append("⚠️ Channel 1 link Error. Contact support.")

    # FORCE_SUB_CHANNEL 2
    if FORCE_SUB_CHANNEL2:
        try:
            member = await client.get_chat_member(chat_id=FORCE_SUB_CHANNEL2, user_id=user_id)
            if member.status in {ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER}:
                status_list.append("🔹 Channel 1 - ✅ Joined")
            else:
                raise UserNotParticipant
        except UserNotParticipant:
            user = await jishuboty().get_user(user_id)
            if user and user["user_id"] == user_id:
                status_list.append("🔹 Channel 2 - ✅ Requested")
            else:
                # check cached link from DB
                invite_info = await req_collection.find_one({"channel_id": FORCE_SUB_CHANNEL2})
                invite_link = invite_info.get("invite_link") if invite_info else None
                expires_at = invite_info.get("expires_at") if invite_info else None
    
                if not invite_link or not expires_at or datetime.utcnow() > expires_at:
                    try:
                        expire_at = datetime.utcnow() + timedelta(hours=1)
                        join_request_link = await client.create_chat_invite_link(
                            chat_id=FORCE_SUB_CHANNEL2,
                            creates_join_request=True,
                            expire_date=expire_at
                        )
                        invite_link = join_request_link.invite_link
                        await req_collection.update_one(
                            {"channel_id": FORCE_SUB_CHANNEL2},
                            {"$set": {"invite_link": invite_link, "expires_at": expire_at}},
                            upsert=True
                        )
                        # Notify admins about the link reset
                        for admin_id in ADMINS:
                            try:
                                await client.send_message(
                                    chat_id=admin_id,
                                    text=f"<b>Invite link for channel {FORCE_SUB_CHANNEL2} has been reset.\nNew link: {invite_link}</b>",
                                    disable_web_page_preview=True
                                )
                            except Exception as e:
                                print(f"[Notify Admin Fallback Error] {admin_id}: {e}")
                    except Exception as e:
                        print(f"[JoinRequest1 Failed] {e}")
                        try:
                            invite_link = await client.export_chat_invite_link(FORCE_SUB_CHANNEL2)
                        except Exception as e2:
                            print(f"[Export1 Failed] {e2}")
    
                status_list.append("🔹 Channel 2 - ❌ Not Joined")
                if invite_link:
                    temp_buttons.append(InlineKeyboardButton("Join Channel 2", url=invite_link))
                else:
                    status_list.append("⚠️ Channel 2 link Error. Contact support.")

    
    # FORCE_SUB_CHANNEL 3
    if FORCE_SUB_CHANNEL3:
        try:
            member = await client.get_chat_member(chat_id=FORCE_SUB_CHANNEL3, user_id=user_id)
            if member.status in {ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER}:
                status_list.append("🔹 Channel 3 - ✅ Joined")
            else:
                raise UserNotParticipant
        except UserNotParticipant:
            user = await jishubotx().get_user(user_id)
            if user and user["user_id"] == user_id:
                status_list.append("🔹 Channel 3 - ✅ Requested")
            else:
                # check cached link from DB
                invite_info = await req_collection.find_one({"channel_id": FORCE_SUB_CHANNEL3})
                invite_link = invite_info.get("invite_link") if invite_info else None
                expires_at = invite_info.get("expires_at") if invite_info else None
    
                if not invite_link or not expires_at or datetime.utcnow() > expires_at:
                    try:
                        expire_at = datetime.utcnow() + timedelta(hours=1)
                        join_request_link = await client.create_chat_invite_link(
                            chat_id=FORCE_SUB_CHANNEL3,
                            creates_join_request=True,
                            expire_date=expire_at
                        )
                        invite_link = join_request_link.invite_link
                        await req_collection.update_one(
                            {"channel_id": FORCE_SUB_CHANNEL3},
                            {"$set": {"invite_link": invite_link, "expires_at": expire_at}},
                            upsert=True
                        )
                        for admin_id in ADMINS:
                            try:
                                await client.send_message(
                                    chat_id=admin_id,
                                    text=f"<b>Invite link for channel {FORCE_SUB_CHANNEL3} has been reset.\nNew link: {invite_link}</b>",
                                    disable_web_page_preview=True
                                )
                            except Exception as e:
                                print(f"[Notify Admin Fallback Error] {admin_id}: {e}")
                    except Exception as e:
                        print(f"[JoinRequest1 Failed] {e}")
                        try:
                            invite_link = await client.export_chat_invite_link(FORCE_SUB_CHANNEL3)
                        except Exception as e2:
                            print(f"[Export1 Failed] {e2}")
    
                status_list.append("🔹 Channel 3 - ❌ Not Joined")
                if invite_link:
                    temp_buttons.append(InlineKeyboardButton("Join Channel 3", url=invite_link))
                else:
                    status_list.append("⚠️ Channel 3 link Error. Contact support.")



    # Add Refresh button
    temp_buttons.append(InlineKeyboardButton("↺ Refresh", callback_data="refresh_status"))

    # Add Get File button if command has extra argument
    try:
        temp_buttons.append(
            InlineKeyboardButton(
                text='↺ Get File',
                url=f"https://t.me/{client.username}?start={message.command[1]}"
            )
        )
        last_cmd = message.command[1]
        database.cmd_data.update_one(
            {"user_id": user_id},
            {"$set": {"last_cmd": last_cmd}},
            upsert=True
        )
    except IndexError:
        pass

    # Split buttons into rows with 2 buttons each
    buttons = [temp_buttons[i:i+2] for i in range(0, len(temp_buttons), 2)]

    # Compose status message
    # if all("✅ 𝖩𝗈𝗂𝗇𝖾𝖽" in status for status in status_list):
    #     caption = (
    #         f"{FORCE_MSG.format(status_list='\n'.join(status_list), mention=message.from_user.mention)}\n\n"
    #         f"🎉 You can now use the bot!"
    #     )
    # else:
    caption = FORCE_MSG.format(status_list="\n".join(status_list), mention=message.from_user.mention)

    # Reply with message and buttons
    try:
        await message.reply_text(
            text=caption,
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True,
        )
    except Exception as e:
        print(f"Error sending reply: {e}")



@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
