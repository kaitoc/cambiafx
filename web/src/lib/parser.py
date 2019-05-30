import requests, json
from bs4 import BeautifulSoup
from collections import defaultdict
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False, use_cache_server=False)

URL_INVERSTING = "https://es.investing.com/currencies/usd-pen"
URL_CUANTODOLAR = "https://cuantoestaeldolar.pe"
URL_BLOOMBERG = "https://www.bloomberg.com/markets2/api/datastrip/PEN%3ACUR%2CUSD%3ACUR%2CINDU%3AIND?locale=en&customTickerList=true"

REF_BLOOMBERG = "https://www.bloomberg.com/quote/USDPEN:CUR"
REF_BLOOMBERG_DATA ="https://www.bloomberg.com/markets2/api/quote/CUR/USDPEN%3ACUR?locale=en"
UA_MAC = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15"
UA_LINUX = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"

def parseBloomberg():
    ua_ = UA_LINUX
    print(f"\tUSER AGENT, bloomberg: {ua_}")

    bloomberg = requests.get(
        URL_BLOOMBERG, headers={
            "User-Agent": ua_,
            "Accept": "*/*"
        })
    sb = BeautifulSoup(bloomberg.text, 'html.parser')
    b_json = json.loads(sb.text)[0]

    tables_json = [{
        "title": "Bloomberg",
        "real_time": [b_json["price"]],
        "var": [b_json["priceChange1Day"]],
        "rango":[b_json["lowPrice"], b_json["highPrice"]]}]

    return tables_json

def parseInvesting():
    ua_ = ua.random
    print(f"\tUSER AGENT, investing: {ua_}")

    investing = requests.get(URL_INVERSTING, headers={"User-Agent": ua_})

    sinv = BeautifulSoup(investing.text, 'html.parser')
    divisa = sinv.find("span", {"id": "last_last"})
    var = sinv.find("span",{"class": "arial_20 greenFont pid-2177-pc", "dir": "ltr"})
    tables_json = []

    container = sinv.find("div", {"id":"quotes_summary_secondary_data"})
    
    for l0, li in enumerate(container.div.ul):
        for s0, span in enumerate(li):
            if l0 == 1 and s0 == 2:
                tables_json.append({
                        "title": "Investing",
                        "real_time" : [divisa.contents[0]],
                        "var" : [var.contents[0]],
                        "cierre": [span.contents[0]],
                        "compra": [],
                        "venta": [],
                        "rango": []
                    })
            if l0 == 3 and s0 == 2:
                compra = span.find("span", {"class":"inlineblock pid-2177-bid"})
                venta = span.find("span", {"class":"inlineblock pid-2177-ask"})
                tables_json[0]["compra"].append(compra.contents[0])
                tables_json[0]["venta"].append(venta.contents[0])
            if l0 == 5 and s0 == 2:
                rango_min = span.find("span", {"class":"inlineblock pid-2177-low"})
                rango_max = span.find("span", {"class":"inlineblock pid-2177-high"})
                tables_json[0]["rango"].append([rango_min.contents[0], rango_max.contents[0]])
    return tables_json


def parseCuantodolar():
    ua_ = ua.random
    print(f"\tUSER AGENT, cuantodolar: {ua_}")

    cuantodolar = requests.get(URL_CUANTODOLAR, headers={"User-Agent": ua_})

    scd = BeautifulSoup(cuantodolar.text, 'html.parser')
    containers = scd.findAll("div", {"class": "cont_cambio"})

    tables = []
    for container in containers:
        tables.append(container.find('table'))

    tables_json = []
    for t0, table in enumerate(tables[:3]):
        for r0, tr in enumerate(table.findAll('tr')):
            for c0, td in enumerate(tr.findAll('td')):
                if r0 == 0:
                    if c0 == 0:
                        tables_json.append({
                            "title": td.get_text(),
                            "entidad": [],
                            "compra": [],
                            "venta": []
                        })

                elif c0 == 0:
                    img = td.find("img")
                    if (img and img.has_attr('alt')):
                        tables_json[t0]["entidad"].append(
                            td.find("img").get('alt', ''))
                    else:
                        tables_json[t0]["entidad"].append(td.get_text().replace("\n", ""))
                elif c0 == 1:
                    tables_json[t0]["compra"].append(td.get_text().replace("\n", "").strip())
                elif c0 == 2:
                    tables_json[t0]["venta"].append(td.get_text().replace("\n", "").strip())
    return tables_json

