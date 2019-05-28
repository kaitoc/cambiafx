import requests, json
from bs4 import BeautifulSoup
from collections import defaultdict
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False, use_cache_server=False)

URL_INVERSTING = "https://es.investing.com/currencies/usd-pen"
URL_CUANTODOLAR = "https://cuantoestaeldolar.pe"
URL_BLOOMBERG = "https://www.bloomberg.com/markets2/api/datastrip/PEN%3ACUR%2CUSD%3ACUR%2CINDU%3AIND?locale=en&customTickerList=true"

REF_BLOOMBERG = "https://www.bloomberg.com/quote/USDPEN:CUR"
UA_MAC = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15"


def parseBloomberg():
    ua_ = UA_MAC
    print(f"\tUSER AGENT, bloomberg: {ua_}")

    bloomberg = requests.get(
        URL_BLOOMBERG, headers={
            "User-Agent": ua_,
            "Referer": REF_BLOOMBERG
        })
    sb = BeautifulSoup(bloomberg.text, 'html.parser')
    print(sb.prettify())
    return json.loads(sb.text)


def parseInvesting():

    ua_ = ua.random
    print(f"\tUSER AGENT, investing: {ua_}")

    investing = requests.get(URL_INVERSTING, headers={"User-Agent": ua_})

    sinv = BeautifulSoup(investing.text, 'html.parser')
    return sinv

import requests, json
from bs4 import BeautifulSoup
from collections import defaultdict
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False, use_cache_server=False)

URL_INVERSTING = "https://es.investing.com/currencies/usd-pen"
URL_CUANTODOLAR = "https://cuantoestaeldolar.pe"
URL_BLOOMBERG = "https://www.bloomberg.com/markets2/api/datastrip/PEN%3ACUR%2CUSD%3ACUR%2CINDU%3AIND?locale=en&customTickerList=true"

REF_BLOOMBERG = "https://www.bloomberg.com/quote/USDPEN:CUR"
UA_MAC = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15"


def parseBloomberg():
    ua_ = UA_MAC
    print(f"\tUSER AGENT, bloomberg: {ua_}")

    bloomberg = requests.get(
        URL_BLOOMBERG, headers={
            "User-Agent": ua_,
            "Referer": REF_BLOOMBERG
        })
    sb = BeautifulSoup(bloomberg.text, 'html.parser')
    print(sb.prettify())
    return json.loads(sb.text)


def parseInvesting():

    ua_ = ua.random
    print(f"\tUSER AGENT, investing: {ua_}")

    investing = requests.get(URL_INVERSTING, headers={"User-Agent": ua_})

    sinv = BeautifulSoup(investing.text, 'html.parser')
    return sinv


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
                        tables_json[t0]["entidad"].append(td.get_text())
                elif c0 == 1:
                    tables_json[t0]["compra"].append(td.get_text())
                elif c0 == 2:
                    tables_json[t0]["venta"].append(td.get_text())
    return tables_json

