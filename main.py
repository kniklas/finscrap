import requests
import bs4

# TODO
# - add another page interface
# - add logging errors/info

isin_urls = {
    "analizy.pl": {
        "ISIN1": "https://www.analizy.pl/fundusze-inwestycyjne-otwarte/ALL90/allianz-dochodowy-income-and-growth",  # noqa: E501
        "ISIN2": "https://www.analizy.pl/fundusze-inwestycyjne-otwarte/PCS87E/pko-zabezpieczenia-emerytalnego-2070-e",  # noqa: E501
    }
}

sel = isin_urls['analizy.pl']
for isin in sel.keys():
    resp = requests.get(sel[isin])
    soup = bs4.BeautifulSoup(resp.content, "html.parser")
    date = soup.find("p", class_="lightProductText").text
    price = soup.find("span", class_="productBigText").text

    print("ISIN:", isin, "\tDate:", date, "\tPrice:", price)
