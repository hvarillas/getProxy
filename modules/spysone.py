import requests
from .useragent.uarandom import getIndexUa
from parsel import Selector
from requests_html import HTML


all_types = {
    'ALL': 0,
    'HTTP': 1,
    'SOCKS': 2
}


def getByCountry(country, proxy_type='ALL'):
    proxy_type = proxy_type.upper()
    if proxy_type not in all_types:
        return None
    headers = {
        'User-Agent': getIndexUa(10)
    }
    URL = 'http://spys.one/free-proxy-list/{}/'.format(country.upper())
    token_data = requests.get(URL, headers=headers)
    token_selc = Selector(text=token_data.text)
    token = token_selc.xpath("//input[@type='hidden'and@name='xx0']/@value").extract_first()
    data = {
        'xx0': token,
        'xpp': 5,
        'xf1': 0,
        'xf2': 0,
        'xf4': 0,
        'xf5': all_types[proxy_type]
    }
    headers = {
        'User-Agent': getIndexUa(10),
        'Host': 'spys.one',
        'Content-Length': '66',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'http://spys.one',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': (
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,app'
            'lication/signed-exchange;v=b3;q=0.9'
        ),
        'Referer': 'http://spys.one/free-proxy-list/PE/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Connection': 'close'
    }
    r = requests.post(URL, headers=headers, data=data)
    proxies = []
    if r.ok:
        html = HTML(html=r.text)
        html.render()
        page = Selector(text=html.html)
        table = page.css('tr')
        for tr in table:
            tds = tr.css("td")
            ip = tds[0].css('font::text').extract()
            if len(ip) == 3:
                proxies.append('http://{}:{}'.format(ip[0], ip[2]))
        return proxies
    else:
        return []
