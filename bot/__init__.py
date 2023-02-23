import os
from fnmatch import fnmatch

import nextcord
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True


class Equinox(commands.Bot):
    def __init__(self):
        self.prefix = "!"
        super().__init__(command_prefix=self.prefix, intents=intents)

    def gears(self):
        """Self loads all the cogs in directory"""
        print("adding gears...")
        try:
            gears = [
                "bot.cogs." + os.path.basename(files)[:-3] for files in os.listdir("./bot/cogs")
                if fnmatch(files, "*.py")
            ]

            for gear in gears:
                self.load_extension(gear)
                print(f"...{gear[9:]} gear added")
        except:
            if FileNotFoundError:
                print("...no gear added")

    async def on_connect(self):
        print("conneting...")
        self.gears()

    async def on_ready(self):
        await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="Over"))
        print(bot.user)

    def run(self):
        super().run(os.getenv("bot_token"), reconnect=True)


bot = Equinox()
