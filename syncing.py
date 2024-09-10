import requests
from config import config
import queries as queries

db = config.clients.firestore

def print_access_tokens():
    urls = []
    shopify_store_collection_ref = db.collection("shopify_stores")
    shopify_stores = shopify_store_collection_ref.stream()
    for store in shopify_stores:
        print(store.id, store.get('access_token'))


def fetch_shopify_graphql(myshopify_domain, access_token, query):
    endpoint = 'https://' + myshopify_domain + '/admin/api/2024-07/graphql.json'
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }
    response = requests.post(endpoint, json={'query': query}, headers=headers)
    if response.status_code == 200:
        return response.json()#['data']['products']
    else:
        raise Exception(f"Query failed to run with a {response.status_code}: {response.text}")


if __name__ == '__main__':

    dev_store_myshopify = 'quickstart-4d4c0722.myshopify.com'

    dev_store_ref = db.collection("shopify_stores").document(dev_store_myshopify)
    dev_store = dev_store_ref.get()
    dev_store_access_token = dev_store.get('access_token')

    data = fetch_shopify_graphql(dev_store_myshopify,dev_store_access_token, queries.shopify.productVariant)

    print(data)



