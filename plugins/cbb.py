
from helper_func import *
from pyrogram import __version__, Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ParseMode , ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from database.database import full_userbase
from bot import Bot
from config import *
from plugins.cmd import *

# Callback query handler
@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    mention = query.from_user.mention
    user_id = query.from_user.id

    last_cmd = await database.cmd_data.find_one({"user_id": user_id}, {"last_cmd": 1})  # Fetch the last command from the database
    last_cmd = last_cmd.get("last_cmd") if last_cmd else "default_cmd"  # Default value if no command is found

    if data == "about":
        await query.message.edit_text(
            text=f"ㅤㅤㅤ⌠ 𝗕𝗹𝗼𝗼𝗱𝘀 𝗡𝗲𝘁𝘄𝗼𝗿𝗸 🍀⌡\n\n"
                 f"◉ Bʟᴏᴏᴅs Sɪᴛᴇʀɪᴘ - @{CHANNEL}\n"
                 f"◉ Bʟᴏᴏᴅs Oɴʟʏғᴀɴs - @{SUPPORT_GROUP}</b>"
                 f"◉ Cʀᴇᴀᴛᴇʀ - <a href='tg://user?id={OWNER_ID}'>Saint</a>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔒 Close", callback_data="close")]]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except Exception as e:
            print(f"Error deleting reply-to message: {e}")

    elif data == "premium":
        await query.message.edit_text(
            text="Choose an option:",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Buy Silver", callback_data="buy_silver")],
                    [InlineKeyboardButton("Buy Gold", callback_data="buy_gold")],
                    [InlineKeyboardButton("Buy Diamond", callback_data="buy_diamond")],
                    [InlineKeyboardButton("Close", callback_data="close")]
                ]
            )
        )
    elif data == "buy_silver":
        await query.message.edit_text(
            text=(
                "<b><u>Silver Plan</u></b>\n\n"
                "1 Month - 50 INR\n"
                "<pre>≡ This plan provides premium access for our current bot with no Ads.</pre>\n"
                "⩉ <a href='https://i.ibb.co/nrmbSkG/file-3262.jpg'>Click To Get QR</a>\n"
                "⌕ For other payment methods, contact @odacchi.\n\n"
                "<b>Note: This plan is separate and lets you use bots without verification (Ads) only. Limits will remain the same as before.</b>"
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Back", callback_data="premium")],
                    [InlineKeyboardButton("Close", callback_data="close")]
                ]
            )
        )
    elif data == "buy_gold":
        await query.message.edit_text(
            text=(
                "<b><u>Gold Plan</u></b>\n\n"
                "1 Month - 100 INR\n"
                "<pre>≡ This plan provides premium access for our two bots with no Ads.</pre>\n"
                "⩉ <a href='https://i.ibb.co/nrmbSkG/file-3262.jpg'>Click To Get QR</a>\n"
                "⌕ For other payment methods, contact @odacchi.\n\n"
                "<b>Note: This plan is separate and lets you use bots without verification (Ads) only. Limits will remain the same as before.</b>"
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Back", callback_data="premium")],
                    [InlineKeyboardButton("Close", callback_data="close")]
                ]
            )
        )
    elif data == "buy_diamond":
        await query.message.edit_text(
            text=(
                "<b>Diamond Plan</b>\n\n"
                "1 Month - 150 INR\n"
                "<pre>≡ This plan provides premium access for our bots with no Ads.</pre>\n"
                "⩉<a href='https://i.ibb.co/nrmbSkG/file-3262.jpg'>Click To Get QR</a>\n"
                "⌕ For other payment methods, contact @odacchi.\n\n"
                "<b>Note: This plan is separate and lets you use bots without verification (Ads) only. Limits will remain the same as before.</b>"
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Back", callback_data="premium")],
                    [InlineKeyboardButton("Close", callback_data="close")]
                ]
            )
        )

    elif data == "show_plans":
        await show_plans(client, query.message)
            
    elif data == "refresh_status":
            # Refresh force subscription status
            force_sub_channels = await get_force_sub_channels()
            buttons = []
            temp_buttons = []  # collect all buttons for 2-column layout
            status_list = []
        
            for i, channel_id in enumerate(force_sub_channels):
                try:
                    invite_info = await channels_collection.find_one({"channel_id": channel_id})
                    invite_link = invite_info.get("invite_link") if invite_info else None
                    expires_at = invite_info.get("expires_at") if invite_info else None
        
                    if not invite_link or not expires_at or datetime.utcnow() > expires_at:
                        new_invite_link = await client.export_chat_invite_link(channel_id)
                        expires_at = datetime.utcnow() + timedelta(hours=1)
        
                        await channels_collection.update_one(
                            {"channel_id": channel_id},
                            {"$set": {"invite_link": new_invite_link, "expires_at": expires_at}},
                            upsert=True,
                        )
                        invite_link = new_invite_link
        
                    try:
                        member = await client.get_chat_member(chat_id=channel_id, user_id=user_id)
                        if member.status in {ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER}:
                            status_list.append(f"⭕️ Channel {i + 1} - ✅ Joined")
                        else:
                            status_list.append(f"⭕️ Channel {i + 1} - ❌ Not Joined")
                            temp_buttons.append(InlineKeyboardButton(f"Join Channel {i + 1}", url=invite_link))
                    except Exception:
                        status_list.append(f"⭕️ Channel {i + 1} - ❌ Not Joined")
                        temp_buttons.append(InlineKeyboardButton(f"Join Channel {i + 1}", url=invite_link))
        
                except Exception as e:
                    print(f"Error processing channel {channel_id}: {e}")
                    status_list.append(f"⭕️ Channel {i + 1} - ⚠️ Error")
                    temp_buttons.append(InlineKeyboardButton(f"Error Help {i + 1}", url=f"https://t.me/{OWNER_USERNAME}"))
        
            # Handle join request check for special FORCE_SUB_CHANNELs
            # Check join request / pending status for special FORCE_SUB_CHANNELs
            # Assuming jishubotz(), jishuboty(), jishubotx() return DB clients or handlers with get_user(user_id)
            # We check if user is in the "request list" (not approved yet) and prompt accordingly
    
            # Special JOIN REQUEST channels check
            async def check_request_join(channel_id, db_func, label, attr):
                try:
                    member = await client.get_chat_member(chat_id=channel_id, user_id=user_id)
                    if member.status in {ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER}:
                        status_list.append(f"🔹 {label} - ✅ Joined")
                        return
                    else:
                        raise UserNotParticipant
                except UserNotParticipant:
                    user = await db_func().get_user(user_id)
                    if user and user["user_id"] == user_id:
                        status_list.append(f"🔹 {label} - ✅ Requested")
                        return
                    else:
                        invite_info = await req_collection.find_one({"channel_id": channel_id})
                        invite_link = invite_info.get("invite_link") if invite_info else None
                        expires_at = invite_info.get("expires_at") if invite_info else None
        
                        if not invite_link or not expires_at or datetime.utcnow() > expires_at:
                            try:
                                expire_at = datetime.utcnow() + timedelta(hours=1)
                                join_request_link = await client.create_chat_invite_link(
                                    chat_id=channel_id,
                                    creates_join_request=True,
                                    expire_date=expire_at
                                )
                                invite_link = join_request_link.invite_link
                                await req_collection.update_one(
                                    {"channel_id": channel_id},
                                    {"$set": {"invite_link": invite_link, "expires_at": expire_at}},
                                    upsert=True
                                )
                            except Exception as e:
                                print(f"[JoinRequest Failed] {e}")
                                try:
                                    invite_link = await client.export_chat_invite_link(channel_id)
                                except Exception as e2:
                                    print(f"[Export Fallback Failed] {e2}")
        
                        status_list.append(f"🔹 {label} - ❌ Not Joined")
                        if invite_link:
                            temp_buttons.append(InlineKeyboardButton(f"Join {label}", url=invite_link))
                        else:
                            status_list.append(f"⚠️ {label} Error.")
        
            if FORCE_SUB_CHANNEL:
                await check_request_join(FORCE_SUB_CHANNEL, jishubotz, "Channel 1", "invitelink")
        
            if FORCE_SUB_CHANNEL2:
                await check_request_join(FORCE_SUB_CHANNEL2, jishuboty, "Channel 2", "invitelink2")
        
            if FORCE_SUB_CHANNEL3:
                await check_request_join(FORCE_SUB_CHANNEL3, jishubotx, "Channel 3", "invitelink3")
        
            # Add "Get File" button
            try:
                temp_buttons.append(InlineKeyboardButton(
                    text="↺ Get File",
                    url=f"https://t.me/{client.username}?start={last_cmd.get('last_cmd')}"
                ))
            except Exception:
                pass
        
            keyboard = [temp_buttons[i:i + 2] for i in range(0, len(temp_buttons), 2)]
            keyboard.append([InlineKeyboardButton("↺ Refresh", callback_data="refresh_status")])
        
            caption = FORCE_MSG.format(status_list="\n".join(status_list), mention=mention)
        
            await query.message.edit_text(
                text=caption,
                reply_markup=InlineKeyboardMarkup(keyboard),
                disable_web_page_preview=True
            )
            await query.answer("Status refreshed!", show_alert=True)
