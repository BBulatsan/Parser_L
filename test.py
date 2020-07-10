import requests
from bs4 import BeautifulSoup
import csv

url = 'https://uaot.org.ua'


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    r = requests.get(url, headers=headers)
    return r.text


def write_csv(data):
    with open('as.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['title'],
                         data['price'],
                         data['metro'],
                         data['url']))


def get_all_a(html):
    soup = BeautifulSoup(html, 'lxml')
    a = soup.find_all('a')
    list_a = []
    for i in a:
        try:
            hr = i.get('href').strip()
            if hr.startswith('/'):
                list_a.append(url + hr)
            elif hr.startswith('tel'):
                continue
            else:
                list_a.append(hr)
        except:
            list_a.append('fall')

    return list_a


def check_links(html):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    status = requests.get(url, headers=headers)
    return status


def main():
    all_a = get_all_a(get_html(url))
    for a in all_a:
        print(a)
        cheker = str(check_links(get_html(a)))
        print(cheker)


if __name__ == '__main__':
    main()
