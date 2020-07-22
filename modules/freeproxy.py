import requests
from .useragent.uarandom import getRandomUa
from parsel import Selector
from requests_html import HTML


all_types = [
    'all',
    'http',
    'https',
    'socks',
    'socks4',
    'socks5',
]

def getByCountry(country, proxy_type='all'):
    proxy_type = proxy_type.lower()
    if proxy_type not in all_types:
        return None
    URL = 'http://free-proxy.cz/es/proxylist/country/{}/{}/ping/all'.format(country.upper(), proxy_type)
    print(URL)
    headers = {
        'User-Agent': getRandomUa()
    }
    r = requests.get(URL, headers=headers)
    if r.ok:
        html = HTML(html=r.text)
        html.render()
        page = Selector(text=html.html)
        table = page.css('table#proxy_list tr')
        for tr in table:
            tds = tr.css("td").extract()
            print(len(tds))
            if len(tds) == 11:
                ip = tds[0].xpath("/text").extract_first()
                print(ip)
    else:
        print('Problem!')