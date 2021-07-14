from functools import lru_cache
import requests
import json


@lru_cache(10)
def scrape_walmart_data(query):
    url = "https://walmart2.p.rapidapi.com/search"

    querystring = {"query": query}

    headers = {
        #keys here
    }
    response = requests.request("GET", url, headers=headers, params=querystring)

    walmart_data = json.loads(response.text)
    # print(walmart_data)

    data = walmart_data
    main_list = []
    try:
        for data in data['items']:

            if sub_key_value := data.get("primaryOffer", {}).get("offerPrice"):
                main_list.append({'usItemId': data['usItemId'], 'title': data['title'], 'brand': data['brand'],
                                  'department': data['department'], 'price': data['primaryOffer']['offerPrice'],
                                  'image': data['imageUrl'], 'product_brand': 'walmart'})
        # return main_data
        return main_list
    except Exception as e:
        print(e)

