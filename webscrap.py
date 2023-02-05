import requests
import bs4
import funds as funds
from urllib import request
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError

# TODO
# - add pytest with mocks to requests, test parsing/formatting data, dict, etc.
# - make sure date is stored/parsed in same format
# - add GitHub actions, pre-commit
# - put logic in python module (public) with documented support of fin webs
# - add logging (as option for the package?)

# TODO (later)
# - add method to retrieve NBP currency rates
# - calculate requirements for DB size


class GetAsset:
    def __init__(self, site):
        self.sel = funds.funds_urls[site]
        print(f"Initialize: {site}")

    def get_element(self, soup, tag, class_id):
        d = soup.find(tag, class_id)
        if d is None:
            raise AttributeError(f"Incorrect <{tag}> or class='{class_id}'")
        return d

    def get_data(self):
        d = dict()
        for isin in self.sel.keys():
            try:
                req = request.Request(self.sel[isin])
                urlopen(self.sel[isin])
            except HTTPError as e:
                print(f"{e} | Verify if URL is correct: {req.full_url}")
                date, price = None, None
            except URLError as e:
                print(f"{e} | Verify if domain name is correct: {req.host}")
                date, price = None, None
            else:
                resp = requests.get(self.sel[isin])
                soup = bs4.BeautifulSoup(resp.content, "lxml")
                try:
                    date = self.get_date(soup)
                except (AttributeError, TypeError) as e:
                    print(f"Cannot extract date from {req.full_url} - {e}")
                    date = None

                try:
                    price = self.get_price(soup)
                except (AttributeError, TypeError) as e:
                    print(f"Cannot extract price from: {req.full_url} - {e} -")
                    price = None

                print(f"{isin},{date},{price}")
                d[isin] = (date, price)
        return d


class GetAssetAnalizy(GetAsset):
    def __init__(self, site):
        super().__init__(site)
        self.date_tag = "p"
        self.date_class = "lightProductText"
        self.price_tag = "span"
        self.price_class = "productBigText"

    def get_date(self, soup):
        d = super().get_element(soup, self.date_tag, self.date_class)
        return d.text

    def get_price(self, soup):
        p = super().get_element(soup, self.price_tag, self.price_class)
        return p.text.replace(",", ".")


class GetAssetBiznesR(GetAsset):
    def __init__(self, site):
        super().__init__(site)
        self.date_tag = "time"
        self.date_class = "q_ch_date"
        self.price_tag = "span"
        self.price_class = "q_ch_act"

    def get_date(self, soup):
        d = super().get_element(soup, self.date_tag, self.date_class)
        return d["datetime"][0:10]

    def get_price(self, soup):
        p = super().get_element(soup, self.price_tag, self.price_class)
        return p.text


class GetAssetBorsa(GetAsset):
    def __init__(self, site):
        super().__init__(site)
        self.date_tag = "span"
        self.date_class = "t-text -block -size-xs | -xs"
        self.price_tag = "span"
        self.price_class = "t-text -black-warm-60 -formatPrice"

    def get_date(self, soup):
        d = super().get_element(soup, self.date_tag, self.date_class)
        return d.strong.text[0:8]

    def get_price(self, soup):
        p = super().get_element(soup, self.price_tag, self.price_class)
        return p.strong.text


class GetAssetIShares(GetAsset):
    def __init__(self, site):
        super().__init__(site)
        self.date_tag = "span"
        self.date_class = "header-nav-label navAmount"
        self.price_tag = "span"
        self.price_class = "header-nav-data"

    def get_date(self, soup):
        d = super().get_element(soup, self.date_tag, self.date_class)
        return d.text[11:23].replace(" ", "/").replace(",", "")

    def get_price(self, soup):
        p = super().get_element(soup, self.price_tag, self.price_class)
        return p.text[2:].strip()
