import requests
from bs4 import BeautifulSoup

PROXIES_URL = 'http://free-proxy-list.net'
response = requests.get(PROXIES_URL)
url = 'https://letterboxd.com/'
#print(response.text)
#print(response.status_code)

soup = BeautifulSoup(response.text,'lxml')
table = soup.find('table')

rows = table.find_all('tr')
cols = [[col.text for col in row.find_all('td')] for row in rows]


raw_proxies = []
proxy_index = 0
for col in cols:
    try:
        if col[6] == 'yes':
            raw_proxies.append('https://'+col[0]+':'+col[1])
    except:
        pass

#print(raw_proxies)

""" def fetch(url):
    global proxy_index
    while proxy_index < len(raw_proxies):
        try:
            print('Trying proxy: ', raw_proxies[proxy_index])
            res = requests.get(url, proxies = {'http':raw_proxies[proxy_index]},timeout=5)
            print(res.status_code)
            return res
        except:
            print(f'Bad proxy')
            proxy_index = proxy_index+ 1 """

#fetch(url_try)
"""
for row in grid:
    #every_tds = row.find_all('td').text,
    #print(every_tds)
    ip_adress = every_tds[0]
    print(ip_adress)
    port = every_tds[1]
    proxy_url = f'http://{ip_adress}:{port}'
    raw_proxies.append(proxy_url) """

def make_request(proxy):
    response = requests.get(url, proxies = {'https': proxy})
    print (response.status_code)
    return response if response.status_code == 200 else None


valid_proxies = []
for proxy in raw_proxies:
    response = requests.get(url, proxies = {'http':proxy})
    print(response.status_code)
    if response.status_code == 200:
        valid_proxy = {'https': proxy}
        valid_proxies.append(proxy)
        print(f'{response.status_code} with {proxy} proxy')


print(valid_proxies)
