import requests
import bs4
import funds as funds

# TODO
# - add logging errors/info, see exception handling in Web Scraping with Python
# - add pytest with mocks to requests.get, bs4.BeatutifulSoup, soup.find
# - add method to retrieve NBP currency rates
# - calculate requirements for DB size


class GetAsset():
    def __init__(self, site):
        self.sel = funds.funds_urls[site]
        print(f"Initialize: {site}")

    def get_date(self, soup):
        pass

    def get_price(self, soup):
        pass

    def get_data(self):
        d = dict()
        for isin in self.sel.keys():
            resp = requests.get(self.sel[isin])
            soup = bs4.BeautifulSoup(resp.content, "lxml")
            date = self.get_date(soup)
            price = self.get_price(soup)
            print(f"{isin},{date},{price}")
            d[isin] = (date, price)
        return d


class GetAssetAnalizy(GetAsset):
    def get_date(self, soup):
        return soup.find("p", class_="lightProductText").text

    def get_price(self, soup):
        return soup.find("span",
                         class_="productBigText").text.replace(",", ".")


class GetAssetBiznesR(GetAsset):
    def get_date(self, soup):
        return soup.find("time", class_="q_ch_date")["datetime"][0:10]

    def get_price(self, soup):
        return soup.find("span", class_="q_ch_act").text


class GetAssetBorsa(GetAsset):
    def get_date(self, soup):
        d = soup.find("span", class_="t-text -block -size-xs | -xs")
        return d.strong.text[0:8]

    def get_price(self, soup):
        p = soup.find("span", class_="t-text -black-warm-60 -formatPrice")
        return p.strong.text


class GetAssetIShares(GetAsset):
    def get_date(self, soup):
        d = soup.find("span", class_="header-nav-label navAmount")
        return d.text[11:23].replace(" ", "/").replace(",", "")

    def get_price(self, soup):
        return soup.find("span", class_="header-nav-data").text[2:].strip()


analizy = GetAssetAnalizy('analizy.pl')
print(analizy.get_data())

biznesr = GetAssetBiznesR('biznesradar.pl')
print(biznesr.get_data())

borsa = GetAssetBorsa('borsa')
print(borsa.get_data())

ishares = GetAssetIShares('ishares')
print(ishares.get_data())
