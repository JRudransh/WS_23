DEBUG = True
FILTER = 0.7
get_url = "https://tcesffb3s8.execute-api.ap-south-1.amazonaws.com/dev/productscraping/getinput"
post_url = "https://tcesffb3s8.execute-api.ap-south-1.amazonaws.com/dev/sitestats"

site_data = {
    "amazon": {
        'url': "https://www.amazon.com.au/s?k={}",
        'selector': {
            'items': '.sg-col-4-of-12.s-result-item.s-asin.sg-col-4-of-16.sg-col.sg-col-4-of-20',
            'title': '#productTitle',
            'links': '.a-link-normal.a-text-normal',
            'merchant': '#sellerProfileTriggerId',
            'price': '#price_inside_buybox',
        },
    },

    "harveynorman": {
        'url': "https://www.harveynorman.com.au/catalogsearch/result/?q={}",
        'selector': {
            'items': '.sg-col-4-of-12.s-result-item.s-asin.sg-col-4-of-16.sg-col.sg-col-4-of-20',
            'title': '#productTitle',
            'links': '.a-link-normal.a-text-normal',
            'merchant': '#sellerProfileTriggerId',
            'price': '#price_inside_buybox',
        },
    },

    "thegoodguys": {
        'url': "https://www.thegoodguys.com.au/SearchDispla&catalogId=30000&langId=-1&sType=SimpleSearch"
               "&resultCatEntryType=2&showResultsPage=true&searchSource=Q&pageView=&beginIndex=0&orderBy=0"
               "&pageSize=60&searchTerm={}",
        'selector': {
            'items': '.sg-col-4-of-12.s-result-item.s-asin.sg-col-4-of-16.sg-col.sg-col-4-of-20',
            'title': '#productTitle',
            'links': '.a-link-normal.a-text-normal',
            'merchant': '#sellerProfileTriggerId',
            'price': '#price_inside_buybox',
        },
    },

    "becextech": {
        'url': "https://www.becextech.com.au/catalog/advanced_search_result.php?keywords={}",
        'selector': {
            'items': '.sg-col-4-of-12.s-result-item.s-asin.sg-col-4-of-16.sg-col.sg-col-4-of-20',
            'title': '#productTitle',
            'links': '.a-link-normal.a-text-normal',
            'merchant': '#sellerProfileTriggerId',
            'price': '#price_inside_buybox',
        },
    },

    "catch": {
        'url': "https://www.catch.com.au/search?query={}",
        'selector': {
            'items': '.sg-col-4-of-12.s-result-item.s-asin.sg-col-4-of-16.sg-col.sg-col-4-of-20',
            'title': '#productTitle',
            'links': '.a-link-normal.a-text-normal',
            'merchant': '#sellerProfileTriggerId',
            'price': '#price_inside_buybox',
        },
    },

    "mobileciti": {
        'url': "https://www.mobileciti.com.au/catalogsearch/result/?q={}",
        'selector': {
            'items': '.sg-col-4-of-12.s-result-item.s-asin.sg-col-4-of-16.sg-col.sg-col-4-of-20',
            'title': '#productTitle',
            'links': '.a-link-normal.a-text-normal',
            'merchant': '#sellerProfileTriggerId',
            'price': '#price_inside_buybox',
        },
    },

    "ebay": {
        'url': "https://www.ebay.com.au/sch/i.html?_nkw={}",
        'selector': {
            'items': '.sg-col-4-of-12.s-result-item.s-asin.sg-col-4-of-16.sg-col.sg-col-4-of-20',
            'title': '#productTitle',
            'links': '.a-link-normal.a-text-normal',
            'merchant': '#sellerProfileTriggerId',
            'price': '#price_inside_buybox',
        },
    },

    "jbhifi": {
        'url': "https://www.jbhifi.com.au/?query={}",
        'selector': {
            'items': '.sg-col-4-of-12.s-result-item.s-asin.sg-col-4-of-16.sg-col.sg-col-4-of-20',
            'title': '#productTitle',
            'links': '.a-link-normal.a-text-normal',
            'merchant': '#sellerProfileTriggerId',
            'price': '#price_inside_buybox',
        },
    },

    "officeworks": {
        'url': "https://www.officeworks.com.au/shop/officeworks/search?q={}&view=grid&page=1&sortBy=bestmatch",
        'selector': {
            'items': '.sg-col-4-of-12.s-result-item.s-asin.sg-col-4-of-16.sg-col.sg-col-4-of-20',
            'title': '#productTitle',
            'links': '.a-link-normal.a-text-normal',
            'merchant': '#sellerProfileTriggerId',
            'price': '#price_inside_buybox',
        },
    }
}

debug_data = {
                "responseCode": 200,
                "responseMessage": "get scraping data from rabbitmq successfully",
                "preferencePojo": {
                    "preferenceId": 84,
                    "userId": 1,
                    "url_scrap": "https://www.amazon.com.au/",
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
