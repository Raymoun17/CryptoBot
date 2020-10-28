import discord
from discord.ext import commands
from core.Coin import Coin


class Pairs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def pairs(self, ctx, currency1, currency2):
        coin1 = Coin(currency1)
        coin1.get_data()
        coin2 = Coin(currency2)
        coin2.get_data()
        pair_price = coin1.price / coin2.price
        title = f"{coin1.symbol} / {coin2.symbol} Pair Price\n"
        description = f"1 {coin1.symbol} = {pair_price} {coin2.symbol}"
        color = 0xff0000
        embed = discord.Embed(
            title=title, description=description, color=color)

        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Pairs(bot))
