import requests
from bs4 import BeautifulSoup
from random import choice


def get_html(url, useragent=None, proxy=None):

    r = requests.get(url, headers=useragent, proxies=proxy)
    return r.text


def get_ip(html):
    print('Proxy & User-Agent')
    soup = BeautifulSoup(html, 'lxml')
    ip = soup.find('span', class_='ip').text.strip()
    ua = soup.find('span', class_='ip').find_next_sibling('span').text.strip()
    print(ip)
    print(ua)
    print('--------------------------------------------------')


def main():
    url = 'http://sitespy.ru/my-ip'
    user_agents = open('user_agents.txt').read().split('*')
    proxies = open('proxy_list.txt').read().split('*')
    for i in range(10):
        proxy = {'http': 'http://' + choice(proxies)}
        useragent = {'User-Agent': choice(user_agents)}
        print(proxy)
        try:
            html = get_html(url, useragent, proxy)
        except:
            continue
        get_ip(html)


if __name__ == '__main__':
    main()
