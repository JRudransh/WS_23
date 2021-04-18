from requests_html import HTMLSession
import time
from datetime import datetime
from requests import get, post
from string import punctuation
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from Settings import *
from Functions import Sku


class Scraper:

    name = str
    price = int
    seller = str
    prd = dict
    search_url = str
    time = 0.0
    selector = str
    url_name = str
    comp_price = float
    competition = float
    min_price = float

    SELENIUM = False

    def __init__(self):
        self.given_url = ''
        self.session = HTMLSession()
        self.data_list = []
        self.data_sorted = []
        self.DEBUG = DEBUG

    def get_sku(self, url):
        sku = Sku(url, self.DEBUG)
        get_sku = getattr(sku, self.url_name)
        return get_sku()

    def get_input(self):
        if self.DEBUG:
            data_dict = debug_data
        else:
            while True:
                data_dict = get(get_url).json()
                if data_dict['responseCode'] == 200:
                    break
                else:
                    print('Data not available..')
                    time.sleep(4)
            if data_dict['responseCode'] != 200:
                return False
        self.prd = data_dict['preferencePojo']
        self.name = self.prd['product_scrap']
        self.price = self.prd['price']
        self.seller = self.prd['seller']
        self.given_url = self.prd['url_scrap']
        self.url_name = self.given_url.split('.')[1]
        return True

    def get_links(self):
        self.get_input()

        self.selector = site_data[self.url_name]['selector']

        self.given_url = site_data[self.url_name]['url']

        self.search_url = self.given_url.replace('{}', self.name)

        r = self.session.get(url=self.search_url)

        items = r.html.find(self.selector['items'])

        print(f'{len(items)} Results Found for: {self.name}')

        link_list = []

        for item in items:
            try:
                links = item.find(self.selector['links'])[0].absolute_links
                link = list(links)[0]
                link_list.append(link)
            except Exception as e:
                error = f'{e} in HTML session get links..\n'
                message = 'Error while getting links..'
                print(error, message) if self.DEBUG else print(message)
        return link_list

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
                        print(error, message) if self.DEBUG else print(message)
                        time.sleep(2)
                try:
                    title = self.clean_text(prd_data.html.find(self.selector['title'])[0].text)
                except IndexError as e:
                    error = f'{e} in HTML session get title -- {n}\n'
                    print(error) if self.DEBUG else None

                try:
                    prd_price = self.clean_price(prd_data.html.find(self.selector['price'])[0].text)
                except Exception as e:
                    error = f'{e} in HTML session find Price -- {n}\n'
                    print(error) if self.DEBUG else None
                    prd_price = '0'

                try:
                    merchant = self.clean_text(prd_data.html.find(self.selector['merchant'])[0].text)
                except Exception as e:
                    error = f'{e} in HTML session find Merchant -- {n}\n'
                    print(error) if self.DEBUG else None
                    merchant = 'NA'

                timestamp = datetime.now()
                main = {
                    'name': title,
                    'price': prd_price,
                    'timestamp': timestamp,
                    'merchant': merchant,
                    'time': (datetime.now() - t1).total_seconds(),
                    'url': link
                }
                self.data_list.append(main)
            except AttributeError as e:
                error = f'{e} in HTML session no content found from link -- {n}\n'
                print(error) if self.DEBUG else None

    def sort_price(self):
        price_list = [n['price'] for n in self.data_list]
        try:
            price_list.sort(reverse=False)
        except Exception as e:
            error = f'{e} in Price Sorting...\n'
            print(error) if self.DEBUG else None
        for price in price_list:
            for single_data in self.data_list:
                if single_data['price'] == price and single_data not in self.data_sorted:
                    self.data_sorted.append(single_data)

    @staticmethod
    def clean_text_filter(given_string: str):
        text = ''.join([word for word in given_string if word not in punctuation])
        text = text.lower()
        return text

    @staticmethod
    def cosine_sim_vectors(vec1, vec2):
        vec1 = vec1.reshape(1, -1)
        vec2 = vec2.reshape(1, -1)

        return cosine_similarity(vec1, vec2)[0][0]

    def filter(self):
        t1 = datetime.now()
        print(f'{len(self.data_list)} Data Found', end=' ')
        words = []
        for i in self.data_list:
            words.append(i['name'])

        words.append(self.name)
        cleaned = list(map(self.clean_text_filter, words))
        vectorized = CountVectorizer().fit_transform(cleaned)
        vector = vectorized.toarray()
        original = vector[-1]
        products = vector[:-1]
        filtered = []
        n = 0
        for product in products:
            similarity = self.cosine_sim_vectors(product, original)
            if similarity >= FILTER:
                filtered.append(self.data_list[n])
            n += 1
        ret_data = []
        for i in self.data_list:
            for j in filtered:
                if i == j:
                    ret_data.append(i)
        print(f'{len(ret_data)} will be uploaded..')
        self.sort_price()
        try:
            self.time += (datetime.now() - t1).total_seconds() / len(self.data_list)
        except Exception as e:
            error = f'{e} in get time...\n'
            print(error) if self.DEBUG else None

    def calculate(self):
        p_l = []
        m_l = []
        min_price = '0'
        comp_price = '0'
        comp = 'NA'
        for i in self.data_list:
            if i['price'] != '0':
                p_l.append(i['price'])
                m_l.append((i['merchant'], i['price']))
        try:
            p_l.sort()
            min_price = p_l[0]
            for i in m_l:
                if i[0] == min_price:
                    comp = i[1]
                    break
                else:
                    comp = 'NA'
        except Exception as e:
            print(e)

        try:
            m_p = min_price if float(self.price) >= float(min_price) else self.price
        except Exception as e:
            print(e)
            m_p = min_price

        for i in m_l:
            if i[1] == min_price:
                comp_price = i[1]
                comp = i[0]
                break
        self.min_price, self.competition, self.comp_price = m_p, comp, comp_price

    def post_data(self):
        response = None
        uploaded = False
        upload = ''
        for data in self.data_sorted:
            sub = {
                "siteUrl": self.prd['url_scrap'],
                "productName": data['name'],
                "preferenceId": self.prd['preferenceId'],
                "minPrice": self.min_price,
                "userPrice": self.prd['price'],
                "competitionPrice": self.comp_price,
                "seller": data['merchant'],
                "processing_time": data['time'] + self.time,
                "competionName": self.competition,
                "productUrl": data['url'],
            }

            if float(data['price']) == float(self.comp_price) and not uploaded:
                while True:
                    try:
                        sub['sku'] = self.get_sku(sub['productUrl'])
                        response = post(post_url, json=sub)
                        if response.status_code == 200:
                            print('Unable to reach server, Retrying...')
                            break

                    except Exception as e:
                        error = f'{e} in Posting Data for {sub["productName"]}\n'
                        print(error) if self.DEBUG else None
                        time.sleep(3)

                upload = sub
                uploaded = True
        print(f'\n\nUploaded data:-\n{upload}\n\n')
        time.sleep(5)
        return response

    def run_once(self):
        try:
            self.scrap()
            self.filter()
            self.calculate()
            self.post_data()
        except Exception as e:
            error = f'{e} in Running the main loop\n'
            print(error) if self.DEBUG else None

    def run_loop(self):
        while True:
            self.run_once()

