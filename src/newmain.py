import requests, json
from bs4 import BeautifulSoup
from collections import defaultdict

URL_INVERSTING = "https://es.investing.com/currencies/usd-pen"
URL_CUANTODOLAR = "https://cuantoestaeldolar.pe"
URL_BLOOMBERG = "https://www.bloomberg.com/markets2/api/datastrip/PEN%3ACUR%2CUSD%3ACUR%2CINDU%3AIND?locale=en&customTickerList=true"

UA = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"

REF_BLOOMBERG = "https://www.bloomberg.com/quote/USDPEN:CUR"

def get_platform():
    platforms = {
        'linux1' : 'Linux',
        'linux2' : 'Linux',
        'darwin' : 'OS X',
        'win32' : 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform

    return platforms[sys.platform]


def parseBloomberg():
    bloomberg = requests.get(
        URL_BLOOMBERG,
        headers={
            "User-Agent": UA,
            "Referer": REF_BLOOMBERG
        })
    sb = BeautifulSoup(bloomberg.text, 'html.parser')
    print(sb.prettify())
    return json.loads(sb.text)


def parseInvesting():
    investing = requests.get(
        URL_INVERSTING, headers={"User-Agent": UA})

    sinv = BeautifulSoup(investing.text, 'html.parser')
    return sinv


def parseCuantodolar():
    cuantodolar = requests.get(
        URL_CUANTODOLAR, headers={"User-Agent": UA})

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
    print(json.dumps(tables_json, indent=4))
    return containers


def main():
    # INFO_CUANTODOLAR = parseCuantodolar()
    INFO_BLOOMBERG = parseBloomberg()
    return
    INFO_INVESTING = parseInvesting()


if __name__ == '__main__':
    main()
