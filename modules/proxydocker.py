import requests
from .useragent.uarandom import getRandomUa
from parsel import Selector
from requests_html import HTML


all_types = [
    'all',
    'http-https',
    'http',
    'https',
    'socks',
    'socks4',
    'socks5',
]

def getByCountry(country, proxy_type='all'):
    MAX_PER_PAGE = 20
    proxy_type = proxy_type.lower()
    if proxy_type not in all_types:
        return None
    headers = {
        'User-Agent': getRandomUa()
    }
    js_proxies = []
    with requests.Session() as session:
        # Get token
        session.headers['User-Agent'] = getRandomUa()
        token_data = session.get('https://www.proxydocker.com', headers=headers)
        token_select = Selector(text=token_data.text)
        token = token_select.xpath("//meta[@name='_token']/@content").extract_first()
        URL = 'https://www.proxydocker.com/es/api/proxylist/'
        data = {
            'token': token,
            'country': country,
            'city': 'all',
            'state': 'all',
            'port': 'all',
            'type': proxy_type,
            'anonymity': 'all',
            'need': 'all',
            'page': '1'
        }
        r = session.post(URL, headers=headers, data=data)
        if r.ok:
            proxies = r.json()
            js_proxies.extend(proxies.get('proxies', []))
            number_proxies = proxies.get('rows_count', 0)
            number_pages = number_proxies//MAX_PER_PAGE
            if float(number_pages) != number_proxies/MAX_PER_PAGE:
                number_pages += 1
            for page in range(2, number_pages + 1):
                data['page'] = str(page)
                r = session.post(URL, headers=headers, data=data)
                if r.ok:
                    proxies = r.json()
                    js_proxies.extend(proxies.get('proxies', []))
            return ['http://{}:{}'.format(x['ip'], x['port']) for x in js_proxies]
        else:
            print('Problem!')