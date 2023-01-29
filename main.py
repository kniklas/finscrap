import requests
import bs4

isin_urls = {
    "analizy.pl": {
        "ISIN1": "https://www.analizy.pl/fundusze-inwestycyjne-otwarte/ALL90/allianz-dochodowy-income-and-growth",
        "ISIN2": "https://www.analizy.pl/fundusze-inwestycyjne-otwarte/PCS87E/pko-zabezpieczenia-emerytalnego-2070-e",
    }
}

sel = isin_urls['analizy.pl']
for isin in sel.keys():
    #  print(sel[isin])
    resp = requests.get(sel[isin])
    soup = bs4.BeautifulSoup(resp.content, "html.parser")
    date = soup.find("p", class_="lightProductText").text
    price = soup.find("span", class_="productBigText").text

    print("ISIN:", isin, "\tDate:", date, "\tPrice:", price)

#  s2 = soup.find_all("span", class_="productBigText")
# https://realpython.com/beautiful-soup-web-scraper-python/
# https://realpython.com/beautiful-soup-web-scraper-python/#find-elements-by-html-class-name
