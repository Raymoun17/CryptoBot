import discord
from discord.ext import commands
from matplotlib import pyplot as plt
from core.Coin import Coin
from time import time


class Chart(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def generate_chart(self, currency):
        coin = Coin(currency)
        coin.get_data()
        coin.get_historical_data()
        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
        x_axis = [x[0][:-5].strip() for x in coin.history]
        x_axis.reverse()

        # AX1
        open_price_y_axis = [float(x[1]) for x in coin.history]
        high_price_y_axis = [float(x[2]) for x in coin.history]
        low_price_y_axis = [float(x[3]) for x in coin.history]
        close_price_y_axis = [float(x[4]) for x in coin.history]
        open_price_y_axis.reverse()
        high_price_y_axis.reverse()
        low_price_y_axis.reverse()
        close_price_y_axis.reverse()
        ax1.plot(x_axis, open_price_y_axis, label="Open")
        ax1.plot(x_axis, high_price_y_axis, label="High")
        ax1.plot(x_axis, low_price_y_axis, label="Low")
        ax1.plot(x_axis, close_price_y_axis, label="Close")
        ax1.set_title(f"Historical data for {coin.name}")
        ax1.axes.xaxis.set_visible(False)
        ax1.legend()

        # AX2
        volume_y_axis = [float(x[5]) for x in coin.history]
        market_cap_y_axis = [float(x[6]) for x in coin.history]
        volume_y_axis.reverse()
        market_cap_y_axis.reverse()
        ax2.plot(x_axis, volume_y_axis, label="Volume")
        ax2.plot(x_axis, market_cap_y_axis, label="Market Cap")
        ax2.legend()

        # PLT
        plt.setp(ax1.get_xticklabels(), rotation=90, fontsize=6)
        plt.setp(ax2.get_xticklabels(), rotation=90, fontsize=6)
        plt.ylabel("USD ($)")
        plt.tight_layout()
        plt.subplots_adjust(hspace=0.12)
        plt.savefig('chart.png')
        plt.close()

    @commands.command()
    async def chart(self, ctx, currency):
        self.generate_chart(currency)
        await ctx.send(file=discord.File('chart.png'))


def setup(bot: commands.Bot):
    bot.add_cog(Chart(bot))
