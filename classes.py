from types import SimpleNamespace

import requests
from config import config
import queries as queries

db = config.clients.firestore

shopify_integrations_collection_id = 'shopify_integrations'


class ShopifyIntegration:
    def __init__(self, store_id):
        self.store_id = store_id
        self.myshopify_domain = self.store_id + '.myshopify.com'
        self.graphql_endpoint = 'https://' + self.myshopify_domain + '/admin/api/2024-07/graphql.json'

        # document reference
        self.firestore = db.collection(shopify_integrations_collection_id).document(self.store_id)

        # collection reference
        self.firestore_products = self.firestore.collection('products')

        self._firestore_doc = None
        self._data = None
        self._products = None
        self._access_token = None
        self._feed = None
        self._shop = None

    @property
    def firestore_doc(self):
        if self._firestore_doc:
            pass
        else:
            self._firestore_doc = self.firestore.get()
        return self._firestore_doc

    @property
    def data(self):
        if self._data:
            pass
        else:
            self._data = self.firestore_doc.to_dict()
        return self._data

    @property
    def access_token(self):
        if self._access_token:
            pass  # If property exists, skip function
        else:
            self._access_token = self.data.get('access_token')
        return self._access_token

    @property
    def shop(self):
        if self._shop:
            pass
        else:
            self._shop = self.firestore_doc.get('shop')
        return self._shop

    @property
    def products(self):

        def read_firestore():
            result = {}
            for doc in self.firestore_products.stream():
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

    @property
    def feed(self):
        if self._feed:
            pass
        else:
            self._feed = self.build_feed()
        return self._feed

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

    # https://shopify.dev/docs/api/admin-graphql/2024-07/queries/products
    def sync_products(self, overwrite=False):
        response = self.graphql_fetch(queries.shopify_gql.products_variants_100x100)
        products = response.get('data').get('products').get('nodes')
        for product in products:
            shopify_gid = product.get('id')
            prod_id = shopify_gid.replace('gid://shopify/Product/','')
            if overwrite:
                self.firestore_products.document(prod_id).set(product)
            else:
                self.firestore_products.document(prod_id).set(product, merge=True)

    # https://shopify.dev/docs/api/admin-graphql/2024-07/queries/shop
    def sync_store_info(self):
        response = self.graphql_fetch(queries.shopify_gql.store_info)
        shop = response.get('data').get('shop')
        self.firestore.set({'shop': shop}, merge=True)

    def build_feed(self):
        items = []

        for product_id in self.products:
            product = self.products[product_id]
            variants = product.get('variants').get('nodes')

            variant_image_urls = []
            for variant in variants:
                if variant.get('image'):
                    variant_image_urls.append(variant.get('image').get('url'))

            for variant in variants:
                item = dict()

                item['id'] = variant.get('sku')

                if product.get('seo').get('title'):
                    item['title'] = product.get('seo').get('title')
                else:
                    item['title'] = product.get('title') + ' ' + variant.get('title')

                if product.get('seo').get('description'):
                    item['description'] = product.get('seo').get('description')
                else:
                    item['description'] = product.get('description')

                item['link'] = product.get('onlineStoreUrl') + '?variant=' + variant.get('id').replace(
                    'gid://shopify/ProductVariant/', '')

                if product.get('hasOnlyDefaultVariant'):
                    item['image_link'] = product.get('featuredMedia').get('preview').get('image').get('url')
                else:
                    item['image_link'] = variant.get('image').get('url')

                item['additional_image_links'] = []
                for source in product.get('media').get('nodes'):
                    image_url = source.get('preview').get('image').get('url')
                    if image_url in variant_image_urls:
                        pass
                    else:
                        item['additional_image_links'].append(image_url)

                if variant.get('inventoryItem').get('unitCost'):
                    amount = float(variant.get('inventoryItem').get('unitCost').get('amount'))
                    currency = variant.get('inventoryItem').get('unitCost').get('currencyCode')
                    item['cost_of_goods_sold'] = '{:.2f}'.format(amount) + ' ' + currency

                if variant.get('compareAtPrice'):
                    price = float(variant.get('price'))
                    compare_price = float(variant.get('compareAtPrice'))
                    currency = self.shop.get('currencyCode')
                    if price < compare_price:
                        item['sale_price'] = '{:.2f}'.format(price) + ' ' + currency
                        item['price'] = '{:.2f}'.format(compare_price) + ' ' + currency
                    else:
                        item['price'] = '{:.2f}'.format(price) + ' ' + currency

                if variant.get('availableForSale'):
                    item['availability'] = 'in_stock'
                else:
                    item['availability'] = 'out_of_stock'

                item['brand'] = product.get('vendor')

                for option in variant.get('selectedOptions'):
                    if option.get('name').lower() == 'color':
                        item['color'] = option.get('value')
                    if option.get('name').lower() == 'size':
                        item['size'] = option.get('value')

                if product.get('productType'):
                    item['product_type'] = product.get('productType')



                items.append(item)

        return items

# class DataFeed:
#     def __init__(self, configuration):
#         self.config = configuration
#         self._sources = None
#         self._items = None
#
#     @property
#     def sources(self):
#         return "hello"


if __name__ == '__main__':

    def print_myshopify_domains():
        shopify_integrations_collection_ref = db.collection(shopify_integrations_collection_id)
        shopify_stores = shopify_integrations_collection_ref.stream()
        for store in shopify_stores:
            print(store.id)

    dev_store = ShopifyIntegration('quickstart-4d4c0722')
    fjellmark = ShopifyIntegration('fjellmark')
    # products = []
    # for doc in dev_store.firestore_products.stream():
    #     products.append(doc.to_dict())

    # dev_store.sync_products()
    # fjellmark.sync_products()

    # print(fjellmark.shop)
    # fjellmark.sync_store_info()
    print(fjellmark.feed)
    # doc = dev_store.firestore.get()
    # print(doc.id)
    # print(doc.to_dict())
    # print(type(dev_store.firestore_doc_ref.get()))

    # print(dev_store.firestore_doc.get('property'))



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


