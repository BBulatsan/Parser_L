import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    r = requests.get(url, headers=headers)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    total_pages = soup.find('div', class_='pagination-root-2oCjZ').find_all('span', class_='pagination-item-1WyVp')[
        -2].text
    return int(total_pages)


def write_csv(data):
    with open('avito.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['title'],
                         data['price'],
                         data['metro'],
                         data['url']))


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='snippet-list js-catalog_serp').find_all('div', class_='item__line')
    for ad in ads:
        try:
            title = ad.find('div', class_='description item_table-description').find('h3').text
        except:
            title = ''

        try:
            url = 'https://www.avito.ru' + ad.find('div', class_='description item_table-description').find('h3').find(
                'a').get('href')
        except:
            url = ''

        try:
            price = ad.find('div', class_='snippet-price-row').find('span').text.split('₽')[0].strip()
        except:
            price = ''

        try:
            metro = ad.find('span', class_='item-address-georeferences-item__content').text
        except:
            metro = ''

        data = {'title': title,
                'price': price,
                'metro': metro,
                'url': url}

        # print(data)
        write_csv(data)
        # return data


def main():
    url = 'https://www.avito.ru/moskva/telefony?q=htc&p=1'
    base_url = 'https://www.avito.ru/moskva/telefony?q=htc&'
    page_part = 'p='
    total_pages = get_total_pages(get_html(url))
    for i in range(1, total_pages):
        url_gen = base_url + page_part + str(i)
        print(url_gen + '  Parsed')
        html = get_html(url_gen)
        get_page_data(html)


if __name__ == '__main__':
    main()
