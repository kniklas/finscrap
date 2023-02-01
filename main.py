import requests
import bs4
import funds as funds

# TODO
# - add another page interface
# - add logging errors/info, see exception handling in Web Scraping with Python
# - add pytest with mocks to requests.get, bs4.BeatutifulSoup, soup.find


sel = funds.funds_urls['analizy.pl']
for isin in sel.keys():
    resp = requests.get(sel[isin])
    soup = bs4.BeautifulSoup(resp.content, "html.parser")
    date = soup.find("p", class_="lightProductText").text
    price = soup.find("span", class_="productBigText").text.replace(",", ".")

    #  print("ISIN:", isin, "\tDate:", date, "\tPrice:", price)
    #  print(isin, ",", date, ",", price.replace(",", "."))
    print(f"{isin},{date},{price}")
