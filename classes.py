from types import SimpleNamespace

import requests
from config import config
import queries as queries

db = config.clients.firestore

shopify_integrations_collection_id = 'shopify_integrations'


class ShopifyIntegration:
    def __init__(self, myshopify_domain):
        self.myshopify_domain = myshopify_domain

        self.firestore_doc_ref = db.collection(shopify_integrations_collection_id).document(self.myshopify_domain)
        self._firestore_doc = None

        self.firestore_products_ref = self.firestore_doc_ref.collection('products')
        self._products = None

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

    @property
    def products(self):

        def read_firestore():
            result = {}
            for doc in self.firestore_products_ref.stream():
                result[doc.id] = doc.to_dict()
            return result

        if self._products:
            pass
        else:
            self._products = read_firestore()
            if self._products == {}:
                self.sync_products()
                self._products = read_firestore()

        return self._products

    def graphql_fetch(self, query):
        headers = {
            'Content-Type': 'application/json',
            'X-Shopify-Access-Token': self.access_token
        }
        response = requests.post(self.graphql_endpoint, json={'query': query}, headers=headers)
        if response.status_code == 200 and not response.json().get('errors'):
            return response.json()
        else:
            raise Exception(f"Query failed to run with a {response.status_code}: {response.text}")

    def sync_products(self, overwrite=False):
        response = self.graphql_fetch(queries.shopify_gql.products_variants_100x100)
        products = response.get('data').get('products').get('nodes')
        for product in products:
            shopify_gid = product.get('id')
            prod_id = shopify_gid.replace('gid://shopify/Product/','')
            if overwrite:
                self.firestore_products_ref.document(prod_id).set(product)
            else:
                self.firestore_products_ref.document(prod_id).set(product, merge=True)



class DataFeed:
    def __init__(self, configuration):
        self.config = configuration
        self._sources = None
        self._items = None

    @property
    def sources(self):
        return "hello"



if __name__ == '__main__':

    def print_myshopify_domains():
        shopify_integrations_collection_ref = db.collection(shopify_integrations_collection_id)
        shopify_stores = shopify_integrations_collection_ref.stream()
        for store in shopify_stores:
            print(store.id)

    dev_store = ShopifyIntegration('quickstart-4d4c0722.myshopify.com')
    # products = []
    # for doc in dev_store.firestore_products_ref.stream():
    #     products.append(doc.to_dict())

    # print(dev_store.sync_products())

    # print(dev_store.products.get('8765739794596').get('seo').get('description'))


    # for prod_id in dev_store.products:
    #     if (dev_store.products[prod_id].get('seo').get('title')):
    #         print('seo', dev_store.products[prod_id].get('seo').get('title'))
    #     else:
    #         print('main', dev_store.products[prod_id].get('title'))






    # This query is limited to 100 products and 100 variants per product. See query.py
    # If you need to break that limit, look at implementing pagination
    # https://shopify.dev/docs/api/usage/pagination-graphql
    # response = dev_store.graphql_fetch(queries.shopify_gql.products_100)
    # print(response)
    # print(response.get('errors'))
    # print(response.get('data').get('products').get('nodes'))

    # print(dev_store.firestore_doc.get('property'))
    # print(dev_store.access_token)

    # sub_collection_ref = dev_store.firestore_doc_ref.collection('new_subcollection')
    #
    # sub_collection_ref.document("001").set({'property':'Testing merge behavior'}, merge=True)

    # sub_collection_ref.do


    # dev_store.sync_products(overwrite=True)


