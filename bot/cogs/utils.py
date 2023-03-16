import nextcord
from nextcord.ext import commands


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Utils(bot))
