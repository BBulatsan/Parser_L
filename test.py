import requests
from bs4 import BeautifulSoup
import csv
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError

base_url = 'https://uaot.org.ua'


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    r = requests.get(url, headers=headers)
    return r.text


def write_csv(data):
    with open('Links_Parsed.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['status'],
                         data['url']))


def get_all_urls(html):
    soup = BeautifulSoup(html, 'lxml')
    a = soup.find_all('a')
    list_urls = []
    for i in a:
        try:
            hr = i.get('href').strip()
            if hr.startswith('/'):
                list_urls.append(base_url + hr)
            elif hr.startswith('tel'):
                continue
            else:
                list_urls.append(hr)
        except:
            print('fall')

    return list(set(list_urls))


def check_links(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    # try:
    #     status = requests.get(url, timeout=(5, 5), headers=headers)
    # except:
    #     print('Time out!')

    adapter = HTTPAdapter(max_retries=3)
    session = requests.Session()

    session.mount(url, adapter)

    try:
        status = session.get(url, headers=headers)
    except ConnectionError as ce:
        print(ce)
    return status.status_code


def main():
    all_a = get_all_urls(get_html(base_url))
    for url in all_a:
        print(url)
        status = check_links(url)
        print(status)
        data = {'status': status,
                'url': url}
        write_csv(data)


if __name__ == '__main__':
    main()
