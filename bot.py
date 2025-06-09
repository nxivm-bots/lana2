from aiohttp import web
from plugins import web_server
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, PORT , CHANNEL_ID , FORCE_SUB_CHANNEL , FORCE_SUB_CHANNEL2 , FORCE_SUB_CHANNEL3
from database.database import *
import pyrogram.utils
from datetime import datetime, timedelta

expire_at = datetime.utcnow() + timedelta(hours=1)
# Expiry setup (used for all channels)
expire_time = datetime.utcnow() + timedelta(hours=1)
# expire_at = int(expire_time.timestamp())

pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        # Channel 1
        if FORCE_SUB_CHANNEL:
            try:
                # First, try to create a join request invite link
                link = await self.create_chat_invite_link(
                    chat_id=FORCE_SUB_CHANNEL, 
                    creates_join_request=True,
                    expire_date=expire_at
                )
                self.invitelink = link.invite_link
                self.invitelink_expiry = expire_time  # Save expiry time
            except Exception as e:
                self.LOGGER(__name__).warning(f"Failed to create a join request invite link: {e}")
                try:
                    self.invitelink = await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    self.LOGGER(__name__).info("Using a regular invite link instead.")
                except Exception as e:
                    self.LOGGER(__name__).warning(f"Failed to export invite link: {e}")
                    self.LOGGER(__name__).warning("Please check if the bot is an admin and has the right permissions!")
                    sys.exit()
        
        # Channel 2
        if FORCE_SUB_CHANNEL2:
            try:
                link = await self.create_chat_invite_link(
                    chat_id=FORCE_SUB_CHANNEL2,
                    creates_join_request=True,
                    expire_date=expire_at
                )
                self.invitelink2 = link.invite_link
                self.invitelink2_expiry = expire_time
            except Exception as e:
                self.LOGGER(__name__).warning(f"Join request link failed (2): {e}")
                try:
                    self.invitelink2 = await self.export_chat_invite_link(FORCE_SUB_CHANNEL2)
                except Exception as e:
                    self.LOGGER(__name__).warning(f"Fallback link export failed (2): {e}")
                    sys.exit()
        
        # Channel 3
        if FORCE_SUB_CHANNEL3:
            try:
                link = await self.create_chat_invite_link(
                    chat_id=FORCE_SUB_CHANNEL3,
                    creates_join_request=True,
                    expire_date=expire_at
                )
                self.invitelink3 = link.invite_link
                self.invitelink3_expiry = expire_time
            except Exception as e:
                self.LOGGER(__name__).warning(f"Join request link failed (3): {e}")
                try:
                    self.invitelink3 = await self.export_chat_invite_link(FORCE_SUB_CHANNEL3)
                except Exception as e:
                    self.LOGGER(__name__).warning(f"Fallback link export failed (3): {e}")
                    sys.exit()

        # Fetch force-subscription channels from the database
        try:
            force_sub_channels = await get_all_force_sub_channels()
            self.force_sub_links = {}
            for channel in force_sub_channels:
                channel_id = channel["channel_id"]
                try:
                    chat = await self.get_chat(channel_id)
                    link = chat.invite_link
                    if not link:
                        link = await self.export_chat_invite_link(channel_id)
                    self.force_sub_links[channel_id] = link
                except Exception as e:
                    self.LOGGER(__name__).warning(f"Failed to fetch invite link for channel {channel_id}: {e}")
        except Exception as e:
            self.LOGGER(__name__).warning(f"Error fetching force-subscription channels from the database: {e}")
            sys.exit()
       
        # Check database channel access
        try:
            #CHANNEL_IDc = await get_config("CHANNEL_ID")
            #CHANNEL_IDc = CHANNEL_ID
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Make sure bot is admin in DB Channel. Current CHANNEL_ID: {CHANNEL_ID}")
            sys.exit()
       
        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info("Bot is running... Created by https://t.me/x0doit")
        self.LOGGER(__name__).info(f"Bot username: @{usr_bot_me.username}")
        self.LOGGER(__name__).info(f""" \n\n 
        bot running...!
(っ◔◡◔)っ ♥ Phdlust ♥
░╚════╝░░╚════╝░╚═════╝░╚══════╝
                                         """)
        self.username = usr_bot_me.username

        # Web server setup
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped. https://t.me/x0doit.")
