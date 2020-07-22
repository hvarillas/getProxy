import requests
from .uarandom import getRandomUa
from parsel import Selector
import time


def getByCountry(country):
    URL = 'https://hidemy.name/es/proxy-list/?country={}'.format(country)
    print(URL)
    headers = {
        'User-Agent': getRandomUa()
    }
    with requests.Session() as session:
        r = session.get(URL, headers=headers)
        time.sleep(6)
        r = session.get(URL, headers=headers)
        if r.ok:
            page = Selector(text=r.text)
            table = page.css('table')
            print(table)
        else:
            print('Problem!')
            print(r.text)
            print(r.status_code)