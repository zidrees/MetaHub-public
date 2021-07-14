import json
from functools import lru_cache

import requests


@lru_cache(10)
def scrape_target_data(query):
    url = "https://target-com-store-product-reviews-locations-data.p.rapidapi.com/product/search"

    querystring = {"store_id": "3991", "keyword": query, "offset": "0", "limit": "2", "sponsored": "1"}

    headers = {
        #rapidapi:keyhere
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    main_list = []
    # print(response.text)
    data = json.loads(response.text)
    # return data
    try:
        for data in data['products'][:10]:
            if sub_key_value := data.get("price", {}).get("formatted_current_price"):
                main_list.append({'usItemId': data['tcin'],
                                  'brand': data['brand'],
                                  'merch_class': data['merch_class'],
                                  'title': data['title'],
                                  # print(data['description'])
                                  'image': data['images'][0]['base_url'],
                                  'primary_image': data['images'][0]['primary'],
                                  'price': data['price']['formatted_current_price'][1:6],
                                  'product_brand': 'target'})

        return main_list
    except Exception as e:
        print(e)

# scrape_target_data("82826299")
