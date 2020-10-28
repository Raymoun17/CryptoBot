import discord
from discord.ext import commands
from core.Coin import Coin


class Price(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def price(self, ctx, currency):
        coin = Coin(currency)
        coin.get_data()
        title = f"1 {coin.name} = {coin.price}$"
        color = 0xff0000
        embed = discord.Embed(
            title=title, color=color)

        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Price(bot))
