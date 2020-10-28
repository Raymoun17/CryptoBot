import discord
from discord.ext import commands
from core.Coin import Coin
import asyncio


class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx, currency):
        coin = Coin(currency)
        coin.get_data()
        title = f"Detailed {coin.name} Info Panel\n"
        description = ""
        # CONSTRUCT THE EMBED DESCRIPTION
        for i in coin.info:
            description += f"{i}\n\n"
        color = 0xff0000
        embed = discord.Embed(
            title=title, description=description, color=color)
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Info(bot))
