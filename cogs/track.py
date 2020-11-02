import discord
from discord.ext import commands
from core.Coin import Coin
import asyncio
import requests
from bs4 import BeautifulSoup as bs


class Track(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.is_tracking = False
        self.currencies = []
        self.delay = 10  # 1 HOUR

    def get_currencies(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0"}

        url = "https://coinmarketcap.com/"
        page = requests.get(url, headers=headers)
        soup = bs(page.content, "lxml")
        currencies = soup.find_all(
            "tr", class_="rc-table-row rc-table-row-level-0 cmc-table-row")

        for currency in currencies:
            data = currency.get_text(separator=u' ').split(" ")
            name = data[1]
            symbol = data[3]
            price = data[4]
            change = data[5]
            coin = Coin(name, symbol, price, change)
            self.currencies.append(coin)

    @commands.command()
    async def track(self, ctx):
        if not self.is_tracking:
            self.is_tracking = True
            await ctx.send("Tracking Crypto!")
            while self.is_tracking:
                self.get_currencies()
                title = "Top 100 Crypto prices"
                description = ""
                color = 0xff0000
                # CONSTRUCT THE EMBED DESCRIPTION
                for currency in self.currencies:
                    description += f"{currency.symbol} = {currency.price}$\n"

                embed = discord.Embed(
                    title=title, description=description, color=color)

                crypto_channel = discord.utils.get(
                    ctx.guild.channels, name="crypto")

                if crypto_channel is None:
                    guild = ctx.guild
                    crypto_channel = await guild.create_text_channel('crypto')
                    await crypto_channel.send(embed=embed)
                    await asyncio.sleep(self.delay)
                else:
                    await crypto_channel.send(embed=embed)
                    await asyncio.sleep(self.delay)
        else:
            await ctx.send("Already tracking Crypto!")


def setup(bot: commands.Bot):
    #bot.add_cog(Track(bot))
    pass
