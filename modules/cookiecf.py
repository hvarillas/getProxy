import requests
from parsel import Selector


def getCookie(url, user_agent=None):
    URL = url
    with requests.Session() as session:
        if user_agent:
            session.headers['User-Agent'] = user_agent
        r = session.get(url)
        page = Selector(text=r.text)
        action = page.xpath('//form/@action').extract_first()
        value_r = page.xpath("//form/input[@name='r'and@type='hidden']/@value").extract_first()
        jschl_vc = page.xpath("//form/input[@name='jschl_vc'and@type='hidden']/@value").extract_first()
        value_pass = page.xpath("//form/input[@name='pass'and@type='hidden']/@value").extract_first()
        if all([
            action,
            value_r,
            jschl_vc,
            value_pass
        ]):
            print(r.headers)

