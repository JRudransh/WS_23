from requests_html import HTMLSession
import time
from datetime import datetime
from requests import get, post
from string import punctuation
from Settings import *


class Scraper:
    def __init__(self, url):
        self.selector = {}
        self.prd = dict
        self.given_url = url
        self.session = HTMLSession()
        self.siteName = str
        self.DEBUG = DEBUG
        self.data = dict
        self.sku = ''
        self.prd_data = None

    def get_sku(self):
        sku = ''
        self.sku = sku

    @staticmethod
    def clean_text(string: str):
        text = ''
        for char in string:
            if char not in punctuation.replace('()', '').replace('&', ''):
                text = text + char
        return text

    def clean_price(self, string: str):
        price = ''
        acceptable = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']
        for char in string:
            if char in acceptable:
                price = price + char

        p = price.split('.')
        if len(p) <= 2:
            return price
        else:
            main_price = f'{p[0]}.{p[1]}'
            return self.clean_price(main_price)

    def scrap(self):
        title = ''
        prd_price = 0
        merchant = 'NA'

        try:
            t1 = datetime.now()
            while True:
                try:
                    self.prd_data = self.session.get(self.given_url)
                    break
                except Exception as e:
                    error = f'{e} in HTML session get link\n'
                    message = 'Error while getting data..\nRetrying in 2 seconds..'
                    print(error, message) if self.DEBUG else print(message)
                    time.sleep(2)
            try:
                title = self.clean_text(self.prd_data.html.find(self.selector['title'])[0].text)
            except IndexError as e:
                error = f'{e} in HTML session get title\n'
                print(error) if self.DEBUG else None

            try:
                prd_price = self.clean_price(self.prd_data.html.find(self.selector['price'])[0].text)
            except Exception as e:
                error = f'{e} in HTML session find Price\n'
                print(error) if self.DEBUG else None

            try:
                merchant = self.clean_text(self.prd_data.html.find(self.selector['merchant'])[0].text)
            except Exception as e:
                error = f'{e} in HTML session find Merchant\n'
                print(error) if self.DEBUG else None

            timestamp = datetime.now()
            self.data = {
                'name': title,
                'price': prd_price,
                'timestamp': timestamp,
                'merchant': merchant,
                'time': (datetime.now() - t1).total_seconds(),
                'url': self.given_url
            }
        except Exception as e:
            error = f'{e} in Scrap Method\n'
            print(error) if self.DEBUG else None

    def post_data(self):
        sub = {
            "productName": self.data['name'],
            "price": self.data['price'],
            "seller": self.data['merchant'],
            "productUrl": self.data['url'],
        }

        while True:
            try:
                sub['sku'] = self.get_sku()
                response = post(post_url, json=sub)
                if response.status_code == 200:
                    print('Unable to reach server, Retrying...')
                    break

            except Exception as e:
                error = f'{e} in Posting Data for {sub["productName"]}\n'
                print(error) if self.DEBUG else None
                time.sleep(3)

        print(f'\n\nUploaded data:-\n{sub}\n\n')
        time.sleep(5)
        return response

    def run(self):
        try:
            self.scrap()
            self.post_data()
        except Exception as e:
            error = f'{e} in Running the main loop\n'
            print(error) if self.DEBUG else None


def get_input():
    while True:
        data_dict = get(get_url).json()
        if data_dict['responseCode'] == 200:
            break
        else:
            print('Data not available..')
            time.sleep(4)
    if data_dict['responseCode'] != 200:
        return False
    name = data_dict['siteName']
    url = data_dict['url_scrap']
    return name, url
