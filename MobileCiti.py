from requests_html import HTMLSession
from datetime import datetime
from Functions import clean_text, clean_price


def get_prd_data(given_name: str, given_url: str):
    session = HTMLSession()

    inp_name = given_name.replace(' ', '+').lower()

    search_url = given_url + inp_name

    r = session.get(url=search_url)

    items = r.html.find(".item.product.product-item")

    print(f'{len(items)} Data Found for: {given_name}')

    # link_list = []
    #
    # for item in items:
    #     try:
    #         links = item.find('.name.fn.l_mgn-tb-sm.l_dsp-blc')[0].absolute_links
    #         link = list(links)[0]
    #         link_list.append(link)
    #     except AttributeError:
    #         print('Link not found \n')
    #         print(item.find('.name.fn.l_mgn-tb-sm.l_dsp-blc')[0].text)
    #     except Exception as e:
    #         print(e)

    return items


def scrap(given_name: str, given_url):
    """
    :param given_name:
    :param given_url:
    :return: List of Scraped data, Data error count and Keyword
    """
    data = get_prd_data(given_name, given_url)

    if len(data) < 1:
        return []

    data_list = []
    n = 1
    for prd_data in data:
        print(f'Getting data from link {n} of {len(data)}...')
        n += 1
        try:
            t1 = datetime.now()

            try:
                title = clean_text(prd_data.find('.product-item-link')[0].text)
            except IndexError:
                continue

            try:
                prd_price = clean_price(prd_data.find('.price')[0].text)
            except Exception as e:
                # print(f'\n{e} price\n{title}\n\n')
                prd_price = '0'

            try:
                merchant = clean_text(prd_data.find('.product--seller')[0].text)
            except Exception as e:
                # print(f'\n\n{e} marchant \n{title}\n\n')
                merchant = 'NA'

            timestamp = datetime.now()
            main = {
                'name': title,
                'price': prd_price,
                'timestamp': timestamp,
                'merchant': merchant,
                'time': (datetime.now() - t1).total_seconds()
            }
            data_list.append(main)
        except AttributeError:
            pass

    return data_list


def run(name, given_url):

    data = scrap(name, given_url)

    return data
