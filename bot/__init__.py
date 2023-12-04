import os
from fnmatch import fnmatch

import nextcord
from nextcord.ext import commands

from logging_config import logger

# Set up intents
intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
testing_guild = ["907379598835208243"]


class Equinox(commands.Bot):
    """
    A Discord bot that extends the commands.Bot class from the nextcord library.
    """

    def __init__(self):
        """
        Initializes the bot with a command prefix and intents.
        """
        self.prefix = "!"
        super().__init__(
            command_prefix=self.prefix, intents=intents, default_guild_ids=testing_guild
        )

    def load_cogs(self):
        """
        Loads all the cogs from the ./bot/cogs directory.
        """
        logger.info("Loading cogs...")
        cogs_dir = "./bot/cogs"
        if not os.path.exists(cogs_dir):
            logger.warning(f"Cog directory '{cogs_dir}' does not exist.")
            return

        for file in os.listdir(cogs_dir):
            if not fnmatch(file, "*.py"):
                continue

            try:
                cog_path = os.path.join("bot", "cogs", file)
                with open(cog_path, "r", encoding="utf-8") as cog_file:
                    self.load_extension(f"bot.cogs.{file[:-3]}")
                    logger.info(f"Cog '{file[:-3]}' loaded")
            except Exception as e:
                logger.error(f"Failed to load cog '{file[:-3]}': {e}")
        logger.info("Done loading cogs.")

    async def on_connect(self):
        """
        Event that fires when the bot successfully connects to the server.
        """
        logger.info("Connecting...")
        self.load_cogs()

    async def on_ready(self):
        """
        Event that fires when the bot is ready to receive commands.
        """
        activity = nextcord.Activity(type=nextcord.ActivityType.watching, name="Over")
        await self.change_presence(activity=activity)
        logger.info(f"Logged in as {self.user}")

    def run(self):
        """
        Starts the bot's event loop and connects to the server using the bot token.
        """
        try:
            token = os.getenv("bot_token")
            if not token:
                raise ValueError("Bot token not found")
            super().run(token, reconnect=True)
        except Exception as e:
            logger.error(f"Failed to run the bot: {e}")


bot = Equinox()
