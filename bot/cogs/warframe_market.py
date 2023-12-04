import nextcord
from nextcord.ext import commands
import requests
from logging_config import logger
import aiohttp, asyncio

base_url = "https://api.warframe.market/v1/items/"


async def fetch_part_data(session, base_url, name, part):
    item_url = f"{base_url}{name.replace(' ', '_').lower()}_prime_{part}/statistics"
    async with session.get(item_url) as response:
        try:
            response.raise_for_status()
            stat_data = (await response.json())["payload"]["statistics_closed"][
                "90days"
            ][-1]
            moving_avg = stat_data["moving_avg"]
            return f"{part.capitalize()}: {moving_avg}\n"
        except (requests.exceptions.HTTPError, KeyError, IndexError) as e:
            return (
                ""  # f"Error fetching data for {name} Prime {part.capitalize()}: {e}\n"
            )
        except Exception as e:
            return ""  # f"An unexpected error occurred: {e}\n"


class MarketPrice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command()
    async def warframe(self, ctx, name: str):
        logger.info("Command used: Warframe")

        frame_parts = {
            "blueprint": "blueprint",
            "neuroptics": "neuroptics",
            "chassis": "chassis",
            "systems": "systems",
            "set": "set",
        }
        tasks = []

        async with aiohttp.ClientSession() as session:
            for part in frame_parts.values():
                tasks.append(fetch_part_data(session, base_url, name, part))

            part_results = await asyncio.gather(*tasks)

        embed_des = "".join(part_results)

        embed = nextcord.Embed(
            title=f"SMA price for {name.capitalize()} Prime",
            description=embed_des,
            color=0x00FF00,  # Green color
        )

        await ctx.send(embed=embed)

    @nextcord.slash_command()
    async def mod(self, ctx, name: str):
        item_url = f"{base_url}{name.replace(' ','_').lower()}/statistics"
        response = requests.get(item_url)
        try:
            response.raise_for_status()
            stat_data = response.json()["payload"]["statistics_closed"]["90days"][-1]
            moving_avg = stat_data["moving_avg"]
            await ctx.send(f"SMA price for {name.capitalize()}: {moving_avg}")
        except requests.exceptions.HTTPError:
            await ctx.send(f"Error fetching data for {name.capitalize()}: {moving_avg}")
        except IndexError:
            await ctx.send(f"Data not available for {name.capitalize()}: {moving_avg}")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")

    @nextcord.slash_command()
    async def weapon(self, ctx, name: str):
        logger.info("Command used Weapon")
        weapons_part = {
            "set": "set",
            "blueprint": "blueprint",
            "blade": "blade",
            "disc": "disc",
            "hilt": "hilt",
            "guard": "guard",
            "grip": "grip",
            "lower_limb": "lower_limb",
            "upper_limb": "upper_limb",
            "string": "string",
            "receiver": "receiver",
            "stock": "stock",
            "barrel": "barrel",
        }
        tasks = []
        async with aiohttp.ClientSession() as session:
            for part in weapons_part.values():
                tasks.append(fetch_part_data(session, base_url, name, part))

            part_results = await asyncio.gather(*tasks)

        embed_des = "".join(part_results)

        embed = nextcord.Embed(
            title=f"SMA price for {name.capitalize()} Prime",
            description=embed_des,
            color=0x00FF00,  # Green color
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MarketPrice(bot))
