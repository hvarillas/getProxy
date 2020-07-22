import requests
from modules.useragent.uarandom import getRandomUa
from modules.cookiecf import getCookie
from modules import spysone, freeproxy, proxydocker

all_proxies = []
# Get proxies of the spysone
spy = spysone.getByCountry('PE')
all_proxies.extend(spy)
# Get proxies of the proxydocker
proxydock = proxydocker.getByCountry('peru', proxy_type='http-https')
all_proxies.extend(proxydock)
# Print all proxies
for x in all_proxies:
    print(x)