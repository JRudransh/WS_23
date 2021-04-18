from requests_html import HTMLSession


class Sku:
    def __init__(self, url, DEBUG):
        self.DEBUG = DEBUG
        session = HTMLSession()
        self.r = session.get(url)

    def amazon(self):
        sku = ''
        try:
            table = self.r.html.find('tr')
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
