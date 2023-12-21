from urllib.parse import urljoin
import requests as r
from bs4 import BeautifulSoup
from urllib import *
import sys
import argparse


try:
    all_urls = set()

    def get_side_urls(url, keyword):
        try:
            response = r.get(url)
        except:
            print(f'Request failed: {url}')
            return

        if response.status_code // 100 == 2:
            soup = BeautifulSoup(response.content, 'html.parser')

            a_tag = soup.find_all('a')
            urls = []
            for tag in a_tag:
                href = tag.get('href')
                if href is not None and href != '':
                    urls.append(href)

            for i in urls:
                if i not in all_urls:
                    all_urls.add(i)
                    url_join = urljoin(url, i)
                    if keyword in url_join:
                        print(url_join)
                        get_side_urls(url_join, keyword)
                else:
                    pass

    def check_domain_access(urls_to_check):
        good_urls = []

        for u in urls_to_check:
            try:
                head = r.head(u, timeout=5)

                if head.status_code // 100 == 2:
                    good_urls.append(u)
                else:
                    print('Bad domain!')
            except r.ConnectionError:
                print('Connection error!')
            except r.RequestException as e:
                print(f'Error for {u}: {e}!')
        print(good_urls)
        return good_urls

    def save_domains(filepath, good_urls):
        with open(filepath, 'w') as file:
            for e in good_urls:
                file.write(e + '\n')


    def main():
        parser = argparse.ArgumentParser(description='Domainsinffer')
        parser.add_argument('-u', metavar='url', type=str, help='enter your url')
        parser.add_argument('-k', metavar='keyword', type=str, help='enter a keyword')
        parser.add_argument('-f', metavar='filepath', type=str, help='enter a filepath')
        args = parser.parse_args()

        url = args.u
        keyword = args.k
        filepath = args.f
        get_side_urls(url, keyword)
        good_urls = check_domain_access(all_urls)
        save_domains(filepath, good_urls)

except KeyboardInterrupt:
    print('programm was been terminated.')
    sys.exit()
    pass

if __name__ == '__main__':
    main()
