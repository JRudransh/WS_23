from requests_html import HTMLSession
from datetime import datetime
import time
from datetime import datetime
from requests import get, post
from string import punctuation
from selenium import webdriver
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from Settings import *
from Functions import clean_text, clean_price


class Scraper:

    name = str
    price = int
    seller = str
    prd = dict

    def __init__(self, given_name: str, given_url: str):
        self.inp_name = given_name.replace(' ', '+').lower()
        self.session = HTMLSession()
        self.search_url = given_url + self.inp_name
        self.given_name = given_name
        self.data_list = []

        self.selector = {
            'items': '.sg-col-4-of-12.s-result-item.s-asin.sg-col-4-of-16.sg-col.sg-col-4-of-20',
            'title': '#productTitle',
            'links': '.a-link-normal.a-text-normal',
            'merchant': '#sellerProfileTriggerId',
            'price': '#price_inside_buybox',
        }

    def get_input(self):
        if DEBUG:
            data_dict = {
                "responseCode": 200,
                "responseMessage": "get scraping data from rabbitmq successfully",
                "preferencePojo": {
                    "preferenceId": 84,
                    "userId": 1,
                    "url_scrap": "https://www.jbhifi.com.au/",
                    "product_scrap": 'Asus Tuf gaming',
                    "createdDate": "2021-02-25 05:34:10",
                    "category": "Mobile",
                    "sku": "sku",
                    "price": 5,
                    "variancepercentage": 0,
                    "status": 0,
                    "seller": "xtrem"
                }
            }
        else:
            while True:
                data_dict = get(get_url).json()
                if data_dict['responseCode'] == 200:
                    break
                else:
                    print('Data not available..')
                    time.sleep(4)
            # For testing
            if data_dict['responseCode'] != 200:
                return False
        self.prd = data_dict['preferencePojo']
        self.name = self.prd['product_scrap']
        self.price = self.prd['price']
        self.seller = self.prd['seller']
        return True

    def get_links(self):
        r = self.session.get(url=self.search_url)

        items = r.html.find(self.selector['items'])

        print(f'{len(items)} Results Found for: {self.given_name}')

        link_list = []

        for item in items:
            try:
                links = item.find(self.selector['links'])[0].absolute_links
                link = list(links)[0]
                link_list.append(link)
            except Exception as e:
                error = f'{e} in HTML session get links..\n'
                message = 'Error while getting links..'
                print(error, message) if DEBUG else print(message)
        return link_list

    @staticmethod
    def find_sku(prd_data):
        lookup_field = 'tr'
        my_table = prd_data.html.find(lookup_field)
        sku = ''
        for row in my_table:
            try:
                th = row.text
                if 'model' in th.lower() and 'number' in th.lower():
                    sku = row.find('td')[0].text
                    break
            except IndexError:
                continue
        return sku

    def scrap(self):
        """
        :return: List of Scraped data, Data error count and Keyword
        """
        links = self.get_links()

        if len(links) < 1:
            return []

        n = 1
        for link in links:
            print(f'Getting data from link {n} of {len(links)}...')
            n += 1
            try:
                t1 = datetime.now()
                while True:
                    try:
                        session = HTMLSession()
                        prd_data = session.get(link)
                        break
                    except Exception as e:
                        error = f'{e} in HTML session get link -- {n}\n'
                        message = 'Error while getting data..\nRetrying in 2 seconds..'
                        print(error, message) if DEBUG else print(message)
                        time.sleep(2)
                try:
                    title = clean_text(prd_data.html.find(self.selector['title'])[0].text)
                except IndexError as e:
                    error = f'{e} in HTML session get title -- {n}\n'
                    print(error) if DEBUG else None
                    continue

                try:
                    sku = self.find_sku(prd_data, n)
                except Exception as e:
                    error = f'{e} in HTML session find SKU -- {n}\n'
                    print(error) if DEBUG else None
                    sku = ''

                try:
                    prd_price = clean_price(prd_data.html.find(self.selector['price'])[0].text)
                except Exception as e:
                    error = f'{e} in HTML session find Price -- {n}\n'
                    print(error) if DEBUG else None
                    prd_price = '0'

                try:
                    merchant = clean_text(prd_data.html.find(self.selector['merchant'])[0].text)
                except Exception as e:
                    error = f'{e} in HTML session find Merchant -- {n}\n'
                    print(error) if DEBUG else None
                    merchant = 'NA'

                timestamp = datetime.now()
                main = {
                    'name': title,
                    'price': prd_price,
                    'timestamp': timestamp,
                    'merchant': merchant,
                    'time': (datetime.now() - t1).total_seconds(),
                    'url': link,
                    'sku': sku,
                }
                self.data_list.append(main)
            except AttributeError as e:
                error = f'{e} in HTML session no content found from link -- {n}\n'
                print(error) if DEBUG else None

    def post_data(self, min_price, competition, comp_price, time_count, url, prd):
        response = None
        uploaded = False
        upload = ''
        for data in self.data_list:
            sub = {
                "siteUrl": url,
                "productName": data['name'],
                "preferenceId": prd['preferenceId'],
                "minPrice": min_price,
                "userPrice": prd['price'],
                "competitionPrice": comp_price,
                "seller": data['merchant'],
                "processing_time": data['time'] + time_count,
                "competionName": competition,
                "productUrl": data['url'],
            }

            if float(data['price']) == float(comp_price) and not uploaded:
                while True:
                    try:
                        response = post(post_url, json=sub)
                        if response.status_code == 200:
                            print('Unable to reach server, Retrying...')
                            break

                    except Exception as e:
                        error = f'{e} in Posting Data for {sub["productName"]}\n'
                        print(error) if DEBUG else None
                        time.sleep(3)

                upload = sub
                uploaded = True
            # For Manual
        print(f'\n\nUploaded data:-\n{upload}\n\n')
        time.sleep(5)
        return response

    def run(self):
        data = self.scrap()
        return data
