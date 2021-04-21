DEBUG = True
get_url = "https://tcesffb3s8.execute-api.ap-south-1.amazonaws.com/dev/productscraping/getinput"
post_url = "https://tcesffb3s8.execute-api.ap-south-1.amazonaws.com/dev/sitestats"

debug_data = {
                "responseCode": 200,
                "responseMessage": "get scraping data from rabbitmq successfully",
                "preferencePojo": {
                    "siteName": 'amazon',
                    "url_scrap": "https://www.amazon.com.au/Xiaomi-DotDisplay-Qualcomm-Snapdragon-Smartphone/dp"
                                 "/B0881TCNX5/ref=sr_1_4?dchild=1&keywords=redmi+9+prime&qid=1618994597&sr=8-4",
                }
}
