import requests, json
from bs4 import BeautifulSoup

URL_INVERSTING = "https://es.investing.com/currencies/usd-pen"
URL_CUANTODOLAR = "https://cuantoestaeldolar.pe"
URL_BLOOMBERG = "https://www.bloomberg.com/markets2/api/datastrip/PEN%3ACUR%2CUSD%3ACUR%2CINDU%3AIND?locale=en&customTickerList=true"

UA_CUANTODOLAR = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15"
UA_BLOOMBERG = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15"
UA_INVESTING = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15"

REF_BLOOMBERG = "https://www.bloomberg.com/quote/USDPEN:CUR"


def parseBloomberg():
    bloomberg = requests.get(
        URL_BLOOMBERG,
        headers={
            "User-Agent": UA_BLOOMBERG,
            "Referer": REF_BLOOMBERG
        })

    sb = BeautifulSoup(bloomberg.text, 'html.parser')

    return json.loads(sb.text)


def parseInvesting():
    investing = requests.get(
        URL_INVERSTING, headers={"User-Agent": UA_INVESTING})

    sinv = BeautifulSoup(investing.text, 'html.parser')
    return sinv


def parseCuantodolar():
    cuantodolar = requests.get(
        URL_CUANTODOLAR, headers={"User-Agent": UA_CUANTODOLAR})

    scd = BeautifulSoup(cuantodolar.text, 'html.parser')
    containers = scd.findAll("div", {"class": "cont_cambio"})
    for container in containers:
        [c.extract() for c in container.findAll('script')]
        print(container.prettify())

    return containers


def main():
    INFO_BLOOMBERG = parseBloomberg()
    INFO_INVESTING = parseInvesting()
    INFO_CUANTODOLAR = parseCuantodolar()


if __name__ == '__main__':
    main()
