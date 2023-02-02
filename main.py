import requests
import bs4
import funds as funds

# TODO
# - check if yahoo works with xlml
# - add another page interface
# - add logging errors/info, see exception handling in Web Scraping with Python
# - add pytest with mocks to requests.get, bs4.BeatutifulSoup, soup.find
# - add method to retrieve NBP currency rates
# - calculate requirements for DB size


#  sel = funds.funds_urls['analizy.pl']
#  for isin in sel.keys():
#      resp = requests.get(sel[isin])
#      soup = bs4.BeautifulSoup(resp.content, "html.parser")
#      date = soup.find("p", class_="lightProductText").text
#      price = soup.find("span", class_="productBigText").text.replace(",", ".")
#      #  print("ISIN:", isin, "\tDate:", date, "\tPrice:", price)
#      print(f"{isin},{date},{price}")

#  sel = funds.funds_urls['biznesradar.pl']
#  for isin in sel.keys():
#      resp = requests.get(sel[isin])
#      soup = bs4.BeautifulSoup(resp.content, "html.parser")
#      date = soup.find("time", class_="q_ch_date")["datetime"][0:10]
#      price = soup.find("span", class_="q_ch_act").text
#      #  print("ISIN:", isin, "\tDate:", date, "\tPrice:", price)
#      print(f"{isin},{date},{price}")

sel = funds.funds_urls['borsa']
for isin in sel.keys():
    resp = requests.get(sel[isin])
    soup = bs4.BeautifulSoup(resp.content, "lxml")
    date = soup.find("span", class_="t-text -block -size-xs | -xs").strong.text[0:8]
    price = soup.find("span", class_="t-text -black-warm-60 -formatPrice").strong.text
    print(f"{isin},{date},{price}")

sel = funds.funds_urls['ishares']
for isin in sel.keys():
    resp = requests.get(sel[isin])
    soup = bs4.BeautifulSoup(resp.content, "lxml")
    date = soup.find("span", class_="header-nav-label navAmount").text[11:23].replace(" ", "/").replace(",", "")
    price = soup.find("span", class_="header-nav-data").text[2:].strip()
    print(f"{isin},{date},{price}")
