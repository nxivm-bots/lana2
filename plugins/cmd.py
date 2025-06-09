# Import required libraries and modules
from bot import Bot
from pyrogram import filters
from config import *
from datetime import datetime
from plugins.start import *
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode
import time

from plugins.join_req import *
from plugins.join_reqy import *
from plugins.join_reqx import *

@Client.on_message(filters.command("total") & filters.private & filters.user(ADMINS))
async def total_all_requests(client: Client, message: Message):
    results = []

    for label, bot in [("X", jishubotx), ("Y", jishuboty), ("Z", jishubotz)]:
        if bot().isActive():
            total = await bot().get_all_users_count()
            results.append(f"**{label}** : `{total}`")

    reply = "**🗿 Total Requests from All Bots:**\n\n" + "\n".join(results)

    await message.reply_text(
        text=reply,
        parse_mode=enums.ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        quote=True
    )
@Client.on_message(filters.command("clear") & filters.private & filters.user(ADMINS))
async def clear_all_requests(client: Client, message: Message):
    cleared = []

    for label, bot in [("X", jishubotx), ("Y", jishuboty), ("Z", jishubotz)]:
        if bot().isActive():
            await bot().delete_all_users()
            cleared.append(f"✅ Cleared : {label}")

    reply = "🧹 **Cleared All Requests:**\n\n" + "\n".join(cleared)

    await message.reply_text(
        text=reply,
        parse_mode=enums.ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        quote=True
    )


@Client.on_message(filters.command("xtotal") & filters.private & filters.user(ADMINS))
async def total_requestsx(client: Client, message: Message):

    if jishubotx().isActive():
        total = await jishubotx().get_all_users_count()
        await message.reply_text(
            text=f"**🗿 Total Requests :** `{total}` : X",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            quote=True)


@Client.on_message(filters.command("xclear") & filters.private & filters.user(ADMINS))
async def purge_requestsx(client: Client, message: Message):
    
    if jishubotx().isActive():
        await jishubotx().delete_all_users()
        await message.reply_text(
            text="Cleared All Requests 🧹 : X",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            quote=True)

@Client.on_message(filters.command("ytotal") & filters.private & filters.user(ADMINS))
async def total_requestsy(client: Client, message: Message):

    if jishuboty().isActive():
        total = await jishuboty().get_all_users_count()
        await message.reply_text(
            text=f"**🗿 Total Requests :** `{total}` : Y",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            quote=True)


@Client.on_message(filters.command("yclear") & filters.private & filters.user(ADMINS))
async def purge_requestsy(client: Client, message: Message):
    
    if jishuboty().isActive():
        await jishuboty().delete_all_users()
        await message.reply_text(
            text="Cleared All Requests 🧹 : Y ",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            quote=True)
        
@Client.on_message(filters.command("ztotal") & filters.private & filters.user(ADMINS))
async def total_requests(client: Client, message: Message):

    if jishubotz().isActive():
        total = await jishubotz().get_all_users_count()
        await message.reply_text(
            text=f"**🗿 Total Requests :** `{total}` : Z",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            quote=True)


@Client.on_message(filters.command("zclear") & filters.private & filters.user(ADMINS))
async def purge_requests(client: Client, message: Message):
    
    if jishubotz().isActive():
        await jishubotz().delete_all_users()
        await message.reply_text(
            text="Cleared All Requests 🧹 : Z",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            quote=True)

'''
@Client.on_message(filters.command('lreset') & filters.private )
async def reset_invite_links(client: Client, message: Message):
    user_id = message.from_user.id

    # Check if the user is an admin or has permission to use the reset command
    if user_id not in ADMINS:  # Replace with your admin check logic
        await message.reply("You do not have permission to use this command.")
        return

    # Retrieve all force subscription channels from the database
    force_sub_channels = await get_force_sub_channels()

    # Reset the invite links for all channels
    for channel_id in force_sub_channels:
        try:
            # Generate a new invite link for each channel
            new_invite_link = await client.export_chat_invite_link(channel_id)
            expires_in = timedelta(hours=1)  # 1-hour validity
            expires_at = datetime.utcnow() + expires_in

            # Update the database with the new invite link and expiration time
            await channels_collection.update_one(
                {'channel_id': channel_id},
                {'$set': {'invite_link': new_invite_link, 'expires_at': expires_at}}
            )
            print(f"Invite link for channel {channel_id} reset successfully.")

        except Exception as e:
            print(f"Error resetting invite link for channel {channel_id}: {e}")

    # Respond back to the user
    await message.reply("Invite links for all channels have been reset successfully.")

'''
@Client.on_message(filters.command('lreset') & filters.private)
async def reset_invite_links(client: Client, message: Message):
    user_id = message.from_user.id

    # Check if the user is an admin
    if user_id not in ADMINS:
        await message.reply("You do not have permission to use this command.")
        return

    force_sub_channels = await get_force_sub_channels()
    success_channels = []

    # Reset invite links for normal channels
    for channel_id in force_sub_channels:
        try:
            new_invite_link = await client.export_chat_invite_link(channel_id)
            expires_at = datetime.utcnow() + timedelta(hours=1)

            await channels_collection.update_one(
                {"channel_id": channel_id},
                {"$set": {"invite_link": new_invite_link, "expires_at": expires_at}},
                upsert=True
            )
            success_channels.append(str(channel_id))
        except Exception as e:
            print(f"[Channel Reset Error] {channel_id}: {e}")

    # Reset invite links for request channels
    req_channels = [FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL2, FORCE_SUB_CHANNEL3]
    for channel_id in req_channels:
        if not channel_id:
            continue
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
            success_channels.append(str(channel_id))
        except Exception as e:
            print(f"[ReqChannel Reset Error] {channel_id}: {e}")
            # Fallback to export_chat_invite_link
            try:
                invite_link = await client.export_chat_invite_link(channel_id)
                fallback_expiry = datetime.utcnow() + timedelta(hours=1)
                await req_collection.update_one(
                    {"channel_id": channel_id},
                    {"$set": {"invite_link": invite_link, "expires_at": fallback_expiry}},
                    upsert=True
                )
                success_channels.append(str(channel_id) + " (fallback)")
            except Exception as e2:
                print(f"[Export Fallback Failed] {channel_id}: {e2}")

    await message.reply(
        f"✅ Invite links reset for channels:\n\n`{', '.join(success_channels)}`",
        quote=True
    )



# Command: Add a new channel
@Client.on_message(filters.command("fadd") & filters.user(ADMINS))
async def add_channel_command(client: Client, message: Message):
    try:
        channel_id = int(message.text.split()[1])
        await add_channel(channel_id)
        await message.reply_text(f"✅ Channel {channel_id} added successfully.")
    except IndexError:
        await message.reply_text("❌ Please provide a channel ID: /fadd <channel_id>")
    except Exception as e:
        await message.reply_text(f"❌ Error adding channel: {e}")

# Command: Remove a channel
@Client.on_message(filters.command("fremove") & filters.user(ADMINS))
async def remove_channel_command(client: Client, message: Message):
    try:
        channel_id = int(message.text.split()[1])
        result = await remove_channel(channel_id)
        if result.deleted_count:
            await message.reply_text(f"✅ Channel {channel_id} removed successfully.")
        else:
            await message.reply_text(f"❌ Channel {channel_id} not found.")
    except IndexError:
        await message.reply_text("❌ Please provide a channel ID: /fremove <channel_id>")
    except Exception as e:
        await message.reply_text(f"❌ Error removing channel: {e}")

# Command: List all channels
@Client.on_message(filters.command("flist") & filters.user(ADMINS))
async def list_channels_command(client: Client, message: Message):
    try:
        channels = await list_channels()
        if not channels:
            await message.reply_text("❌ No channels configured.")
        else:
            channel_list = "\n".join([str(channel) for channel in channels])
            await message.reply_text(f"📜 Current channels:\n{channel_list}")
    except Exception as e:
        await message.reply_text(f"❌ Error listing channels: {e}")

# Command: Reset all channels (clear collection)
@Client.on_message(filters.command("freset") & filters.user(ADMINS))
async def reset_channels_command(client: Client, message: Message):
    try:
        await reset_channels()
        await message.reply_text("✅ All force subscription channels have been reset (cleared).")
    except Exception as e:
        await message.reply_text(f"❌ Error resetting channels: {e}")


# /help command to show available commands
@Bot.on_message(filters.command('help') & filters.private)
async def help_command(bot: Bot, message: Message):
    help_text = """
📖 <b>Bot Command Help</b>

<b>🔰 General Commands:</b>
/start - Start the bot and view a welcome message.
/help - Show this help menu.
/plans - View available premium plans.
/upi - Show UPI payment QR and options.
/myplan - Check your current premium subscription status.
/genlink - Generate a link for a single post.
/batch - Generate links for multiple posts.
/stats - Show bot uptime and statistics.

<b>💠 Premium Commands:</b>
(Available only if you're a premium user)
/myplan - Check your remaining premium time.

<b>🛠 Admin Commands:</b>
/broadcast - Send message to all users.
/users - View total bot user count.
/addpr id days - Add premium to a user.
/removepr id - Remove premium from a user.
/getpremiumusers - List all active premium users.

/lreset - Reset invite links for all force join channels.
/fadd <channel_id> - Add a channel to force join list.
/fremove <channel_id> - Remove a force join channel.
/flist - List all configured force join channels.
/freset - Clear/reset all force join channels.

/xtotal - Show X bot user count.
/xclear - Clear X bot users.
/ytotal - Show Y bot user count.
/yclear - Clear Y bot users.
/total - Show Z bot user count.
/clear - Clear Z bot users.
"""
    await message.reply(help_text, parse_mode=ParseMode.HTML)


# Command to add a premium subscription for a user (admin only)
@Bot.on_message(filters.private & filters.command('addpr') & filters.user(ADMINS))
async def add_premium(bot: Bot, message: Message):
    if message.from_user.id not in ADMINS:
        return await message.reply("You don't have permission to add premium users.")

    try:
        args = message.text.split()
        if len(args) < 3:
            return await message.reply("Usage: /addpr 'user_id' 'duration_in_days'")
        
        target_user_id = int(args[1])
        duration_in_days = int(args[2])
        await add_premium_user(target_user_id, duration_in_days)
        await message.reply(f"User {target_user_id} added to premium for {duration_in_days} days.")
    except Exception as e:
        await message.reply(f"Error: {str(e)}")

# Command to remove a premium subscription for a user (admin only)
@Bot.on_message(filters.private & filters.command('removepr') & filters.user(ADMINS))
async def remove_premium(bot: Bot, message: Message):
    if message.from_user.id not in ADMINS:
        return await message.reply("You don't have permission to remove premium users.")

    try:
        args = message.text.split()
        if len(args) < 2:
            return await message.reply("Usage: /removepr 'user_id'")
        
        target_user_id = int(args[1])
        await remove_premium_user(target_user_id)
        await message.reply(f"User {target_user_id} removed from premium.")
    except Exception as e:
        await message.reply(f"Error: {str(e)}")

@Bot.on_message(filters.command('myplan') & filters.private)
async def my_plan(bot: Bot, message: Message):
    is_premium, expiry_time = await get_user_subscription(message.from_user.id)
    
    if is_premium and expiry_time:
        time_left = int(expiry_time - time.time())
        
        if time_left > 0:
            days_left = time_left // 86400
            hours_left = (time_left % 86400) // 3600
            minutes_left = (time_left % 3600) // 60

            response_text = (
                f"✅ Your premium subscription is active.\n\n"
                f"🕒 Time remaining: {days_left} days, {hours_left} hours, {minutes_left} minutes."
            )
            
            buttons = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Upgrade Plan", callback_data="premium")],
                    [InlineKeyboardButton("🔒 Close", callback_data="close")],
                    [InlineKeyboardButton("Contact Support", url=f"https://t.me/{OWNER}")]
                ]
            )
        else:
            # Subscription expired
            response_text = (
                "⚠️ Your premium subscription has expired.\n\n"
                "Renew your subscription to continue enjoying premium features."
                "\nCheck: /plans"
            )
            
            buttons = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Renew Plan", callback_data="premium")],
                    [InlineKeyboardButton("🔒 Close", callback_data="close")],
                    [InlineKeyboardButton("Contact Support", url=f"https://t.me/{OWNER}")]
                ]
            )

    else:
        # User is not a premium member
        response_text = "❌ You are not a premium user.\nView available plans to upgrade.\n\nClick HERE: /plans"
        
        buttons = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("View Plans", callback_data="premium")],
                [InlineKeyboardButton("🔒 Close", callback_data="close")],
                [InlineKeyboardButton("Contact Support", url=f"https://t.me/{OWNER}")]
            ]
        )

    await message.reply_text(response_text, reply_markup=buttons)


# Command to show subscription plans
@Bot.on_message(filters.command('plans') & filters.private)
async def show_plans(bot: Bot, message: Message):
    plans_text = PAYMENT_TEXT
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("𝖡𝗎𝗒 𝗌𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇 | 𝖭𝗈 𝖠𝖽𝗌", callback_data="premium")],
        [InlineKeyboardButton("Contact Owner", url=f"https://t.me/{OWNER}")],
        [InlineKeyboardButton("🔒 Close", callback_data="close")]
    ])
    await message.reply(plans_text, reply_markup=buttons, parse_mode=ParseMode.HTML)

# Command to show UPI payment QR code and instructions
@Bot.on_message(filters.command('upi') & filters.private)
async def upi_info(bot: Bot, message: Message):
    plans_text = PAYMENT_TEXT
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("𝖡𝗎𝗒 𝗌𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇 | 𝖭𝗈 𝖠𝖽𝗌", callback_data="premium")],
        [InlineKeyboardButton("Contact Owner", url=f"https://t.me/{OWNER}")],
        [InlineKeyboardButton("🔒 Close", callback_data="close")]
    ])
    await message.reply(plans_text, reply_markup=buttons, parse_mode=ParseMode.HTML)

# Command to retrieve a list of active premium users (admin only)
@Bot.on_message(filters.private & filters.command('getpremiumusers') & filters.user(ADMINS))
async def get_premium_users(bot: Bot, message: Message):
    try:
        premium_users = phdlust.find({"is_premium": True, "expiry_time": {"$gt": time.time()}})
        if not phdlust.count_documents({"is_premium": True, "expiry_time": {"$gt": time.time()}}):
            return await message.reply("No active premium users found.")

        users_list = [
            f"User ID: {user.get('user_id')} - Premium Expires in {max(int((user.get('expiry_time') - time.time()) / 86400), 0)} days"
            for user in premium_users
        ]
        await message.reply("<b>Premium Users:</b>\n\n" + "\n".join(users_list), parse_mode=ParseMode.HTML)
    except Exception as e:
        await message.reply(f"Error: {str(e)}")
