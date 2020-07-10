import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from multiprocessing import Pool


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    r = requests.get(url, headers=headers)
    return r.text


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find_all('td',
                        class_='cmc-table__cell cmc-table__cell--sticky cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__name')
    links = []

    for td in tds:
        a = td.find('a').get('href')
        link = 'https://coinmarketcap.com' + a
        links.append(link)

    return links


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = soup.find('h1').text.strip()
    except:
        name = ''
    try:
        price = soup.find('span', class_='cmc-details-panel-price__price').text.strip()
    except:
        price = ''

    data = {'name': name,
            'price': price}
    return data


def write_csv(data):
    with open('coinmarket.csv', 'a') as file:
        writer = csv.writer(file)

        writer.writerow((data['name'],
                         data['price']))
        print(data['name'], 'parsed')

def make_all(url):
    html = get_html(url)
    data = get_page_data(html)
    write_csv(data)


def main():
    start = datetime.now()
    url = 'https://coinmarketcap.com/ru/all/views/all/'
    all_links = get_all_links(get_html(url))
    with Pool(10) as p:
        p.map(make_all, all_links)

    end = datetime.now()
    total = end - start
    print(str(total))


if __name__ == '__main__':
    main()
