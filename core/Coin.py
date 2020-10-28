import requests
from bs4 import BeautifulSoup as bs


class Coin:
    def __init__(self, name, symbol=None, price=None, change=None):
        self.coin_name = name
        self.name = name
        self.symbol = symbol
        self.price = price
        self.change = change
        self.info = []
        self.history = []

    def get_data(self, url=None):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0"}

        if url is None:
            url = f"https://coinmarketcap.com/currencies/{self.name}/"
        else:
            url = f"https://coinmarketcap.com{url}/"

        page = requests.get(url, headers=headers)
        soup = bs(page.content, "lxml")

        name = soup.find_all(
            "div", class_="cmc-details-panel-header__name")[0]
        self.name = name.text.strip()
        self.symbol = name.span.text

        price = soup.find_all(
            "span", class_="cmc-details-panel-price__price")[0].text
        self.price = float(price[1:].replace(",", ""))

        self.change = soup.find_all(
            "span", class_="cmc-details-panel-price__price-change")[0].text

        info = soup.find_all(
            "tr")
        self.info = [x.get_text(separator=u' ') for x in info]

    def get_historical_data(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0"}
        url = f"https://coinmarketcap.com/currencies/{self.coin_name}/historical-data/"
        page = requests.get(url, headers=headers)
        soup = bs(page.content, "lxml")

        rows = [x for x in soup.find_all("tr", class_="cmc-table-row")]
        for row in rows:
            out = []
            for element in row:
                out.append(element.text.replace(",", ""))
            self.history.append(out)
