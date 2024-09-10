import requests
from config import config
import queries as queries

db = config.clients.firestore


class shopifyStore:
    def __init__(self, myshopify_domain):
        self.myshopify_domain = myshopify_domain

        self.firestore_doc_ref = db.collection("shopify_stores").document(self.myshopify_domain)
        self._firestore_doc = None

        self.graphql_endpoint = 'https://' + self.myshopify_domain + '/admin/api/2024-07/graphql.json'
        self._access_token = None

    @property
    def firestore_doc(self):
        if self._firestore_doc:
            pass
        else:
            self._firestore_doc = self.get_firestore_doc()
        return self._firestore_doc

    def get_firestore_doc(self):
        return self.firestore_doc_ref.get()

    @property
    def access_token(self):
        if self._access_token:
            pass  # If property exists, skip function
        else:
            self._access_token = self.get_shopify_access_token()
        return self._access_token

    def get_shopify_access_token(self):
        return self.firestore_doc.get('access_token')

    def graphql_fetch(self, query):
        headers = {
            'Content-Type': 'application/json',
            'X-Shopify-Access-Token': self.access_token
        }
        response = requests.post(self.graphql_endpoint, json={'query': query}, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Query failed to run with a {response.status_code}: {response.text}")



def print_myshopify_domains():
    urls = []
    shopify_store_collection_ref = db.collection("shopify_stores")
    shopify_stores = shopify_store_collection_ref.stream()
    for store in shopify_stores:
        print(store.id)



if __name__ == '__main__':

    dev_store = shopifyStore('quickstart-4d4c0722.myshopify.com')

    data = dev_store.graphql_fetch(queries.shopify.productVariant)

    print(data)

    # print(dev_store.firestore_doc.get('property'))
    # print(dev_store.access_token)



