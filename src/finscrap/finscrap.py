"""Module webscraps financial data from web pages."""

import logging as log
import json
import csv
from urllib import request
from urllib.error import HTTPError
from urllib.error import URLError

import requests
import bs4

# pylint: disable=logging-fstring-interpolation


class GetData:
    """Gets webscrapped data"""

    def __init__(self, funds_json):
        """Create objects to webscrap data."""
        funds = self.load_funds_config(funds_json)
        self.providers = list(funds.keys())
        self.data_dict = {}
        log.basicConfig(level=log.INFO)
        log.info("Initialize GetData")
        log.info(f"Present providers: {self.providers}")
        if "analizy.pl" in self.providers:
            self.analizy_obj = GetAssetAnalizy("analizy.pl", funds)
        if "biznesradar.pl" in self.providers:
            self.biznesr_obj = GetAssetBiznesR("biznesradar.pl", funds)
        if "borsa" in self.providers:
            self.borsa_obj = GetAssetBorsa("borsa", funds)
        if "ishares" in self.providers:
            self.ishares_obj = GetAssetIShares("ishares", funds)

    @staticmethod
    def load_funds_config(funds_json):
        """Load from json file, funds config"""
        with open(funds_json, "r", encoding="utf-8") as fund_config:
            funds_urls = json.load(fund_config)
        return funds_urls

    @staticmethod
    def dict_to_list(data_dict):
        """Covert data result from dictionary to list format, so it could be
        saved as CSV in out_csv() method."""
        asset_list = []
        for asset_id in data_dict:
            list_item = [
                asset_id,
                data_dict[asset_id][0],
                data_dict[asset_id][1],
            ]
            asset_list.append(list_item)
        return asset_list

    def get_data(self):
        """Get data for defined web pages"""
        if "analizy.pl" in self.providers:
            self.data_dict.update(self.analizy_obj.get_data())
        if "biznesradar.pl" in self.providers:
            self.data_dict.update(self.biznesr_obj.get_data())
        if "borsa" in self.providers:
            self.data_dict.update(self.borsa_obj.get_data())
        if "ishares" in self.providers:
            self.data_dict.update(self.ishares_obj.get_data())
        #  print(self.data_dict)

    def out_csv(self, csv_path):
        """Save result to CSV"""
        log.info(f"Saving results to CSV: {csv_path}")
        data_set = self.dict_to_list(self.data_dict)
        #  print(data_set)
        with open(csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(data_set)


class GetAsset:
    """Generic class to get assets"""

    def __init__(self, site, funds):
        """Constructor to initialise site with URL address"""
        self.sel = funds[site]
        log.info(f"Initialize: {site}")

    @staticmethod
    def concatenate_date(day, month, year):
        """Method returns date in YYYY-MM-DD format"""
        return f"{year}-{month}-{day}"

    def get_element(self, soup, tag, class_id):
        """
        Method returns html string if specific tag and class id are found
        """
        element = soup.find(tag, class_id)
        if element is None:
            raise AttributeError(f"Incorrect <{tag}> or class='{class_id}'")
        return element

    def get_data(self):
        """Method returns data scrapped from web pages"""
        data = {}
        for isin in self.sel.keys():
            try:
                # Required to get URL or hostname in error handling
                req = request.Request(self.sel[isin])
                # Catching actual exception
                # pylint: disable=consider-using-with
                request.urlopen(self.sel[isin])
            except HTTPError as exception:
                # pylint: disable=used-before-assignment
                print(
                    f"{exception} | Verify if URL is correct: \
                      {req.full_url}"
                )
                date, price = None, None
            except URLError as exception:
                print(
                    f"{exception} | Verify if domain name is correct: \
                    {req.host}"
                )
                date, price = None, None
            else:
                resp = requests.get(self.sel[isin], timeout=100)
                soup = bs4.BeautifulSoup(resp.content, "lxml")
                # Get date
                try:
                    date = self.get_date(soup)
                except (AttributeError, TypeError) as exception:
                    print(
                        f"Cannot extract date from {req.full_url} - \
                        {exception}"
                    )
                    date = None
                # Get price
                try:
                    price = self.get_price(soup)
                except (AttributeError, TypeError) as exception:
                    print(
                        f"Cannot extract price from: {req.full_url} - \
                        {exception}"
                    )
                    price = None
            data[isin] = (date, price)
            log.info(f"Retrieve: {isin} {date} {price}")
        return data


class GetAssetAnalizy(GetAsset):
    """Specific implementation for analizy.pl"""

    def __init__(self, site, funds):
        """Setup analizy.pl <p> and <span> tags"""
        super().__init__(site, funds)
        self.date_tag = "p"
        self.date_class = "lightProductText"
        self.price_tag = "span"
        self.price_class = "productBigText"

    def get_date(self, soup):
        """Gets date for analizy.pl"""
        date = super().get_element(soup, self.date_tag, self.date_class)
        return self.convert_date(date.text)

    def get_price(self, soup):
        """Gets price for analizy.pl"""
        price = super().get_element(soup, self.price_tag, self.price_class)
        return price.text.replace(",", ".")

    @staticmethod
    def convert_date(input_date):
        """Converts specifically date for analizy.pl"""
        day = input_date[0:2]
        month = input_date[3:5]
        year = input_date[6:10]
        return GetAsset.concatenate_date(day, month, year)


class GetAssetBiznesR(GetAsset):
    """Specific implementation for biznseradar.pl"""

    def __init__(self, site, funds):
        """Setup biznesradar.pl <time> and <span> tags"""
        super().__init__(site, funds)
        self.date_tag = "time"
        self.date_class = "q_ch_date"
        self.price_tag = "span"
        self.price_class = "q_ch_act"

    def get_date(self, soup):
        """Gets date for biznesradar.pl"""
        date = super().get_element(soup, self.date_tag, self.date_class)
        return date["datetime"][0:10]

    def get_price(self, soup):
        """Gets date for biznesradar.pl"""
        price = super().get_element(soup, self.price_tag, self.price_class)
        return price.text


class GetAssetBorsa(GetAsset):
    """Specific implementation for borsa.it"""

    def __init__(self, site, funds):
        """Setup borsa.it <span> tags definitions"""
        super().__init__(site, funds)
        self.date_tag = "span"
        self.date_class = "t-text -block -size-xs | -xs"
        self.price_tag = "span"
        self.price_class = "t-text -black-warm-60 -formatPrice"

    def get_date(self, soup):
        """Gets date for borsa.it"""
        date = super().get_element(soup, self.date_tag, self.date_class)
        return self.convert_date(date.strong.text[0:8])

    def get_price(self, soup):
        """Gets date for borsa.it"""
        price = super().get_element(soup, self.price_tag, self.price_class)
        return price.strong.text

    @staticmethod
    def convert_date(input_date):
        """Static method to covert date in specific manner for borsa.it"""
        day = input_date[6:8]
        month = input_date[3:5]
        year = "20" + input_date[0:2]
        return GetAsset.concatenate_date(day, month, year)


class GetAssetIShares(GetAsset):
    """Class implements specific methods for ishares page"""

    def __init__(self, site, funds):
        """Setup iShares page specific <span> tags"""
        super().__init__(site, funds)
        self.date_tag = "span"
        self.date_class = "header-nav-label navAmount"
        self.price_tag = "span"
        self.price_class = "header-nav-data"

    def get_date(self, soup):
        """Gets date for ishares page"""
        date = super().get_element(soup, self.date_tag, self.date_class)
        cleared_date = date.text[11:23].replace(" ", "/").replace(",", "")
        return self.convert_date(cleared_date)

    def get_price(self, soup):
        """Gets price for ishares page"""
        price = super().get_element(soup, self.price_tag, self.price_class)
        return price.text[2:].strip()

    @staticmethod
    def convert_date(input_date):
        """Static method to covert date in specific manner for iShares"""
        month_dict = {
            "Jan": "01",
            "Feb": "02",
            "Mar": "03",
            "Apr": "04",
            "May": "05",
            "Jun": "06",
            "Jul": "07",
            "Aug": "08",
            "Sep": "09",
            "Oct": "10",
            "Nov": "11",
            "Dec": "12",
        }
        day = input_date[4:6]
        month = month_dict[input_date[0:3]]
        year = input_date[7:11]
        return GetAsset.concatenate_date(day, month, year)
