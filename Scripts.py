from Base import Scraper


class Scripts:
    class Amazon(Scraper):
        def __init__(self, url):
            super().__init__(url)
            self.selector = {
                'items': '.sg-col-4-of-12.s-result-item.s-asin.sg-col-4-of-16.sg-col.sg-col-4-of-20',
                'title': '#productTitle',
                'links': '.a-link-normal.a-text-normal',
                'merchant': '#sellerProfileTriggerId',
                'price': '#price_inside_buybox',
            }

        def get_sku(self):
            sku = ''
            try:
                table = self.prd_data.html.find('tr')
                for row in table:
                    try:
                        th = row.text
                        if 'model' in th.lower() and 'number' in th.lower():
                            sku = row.find('td')[0].text
                            break
                    except IndexError:
                        continue
            except Exception as e:
                error = f'{e} in Getting SKU...\n'
                print(error) if self.DEBUG else None
            return sku

    class Ebay(Scraper):
        def __init__(self, url):
            super().__init__(url)
            self.selector = {
                'items': '.s-item',
                'title': '#itemTitle',
                'links': '.s-item__link',
                'merchant': 'span.mbg-nw',
                'price': '#prcIsum',
            }

        def get_sku(self):
            sku = ''
            try:
                sku = self.prd_data.html.find('#descItemNumber')[0].text
            except Exception as e:
                error = f'{e} in Getting SKU...\n'
                print(error) if self.DEBUG else None
            return sku

