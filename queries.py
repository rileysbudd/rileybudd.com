from types import SimpleNamespace

shopify = SimpleNamespace(**{
    'productVariant':
    """
    query {
        productVariants(first: 3) {
            nodes {
                id
                title
                price
            }
        }
    }
    """
})

if __name__ == '__main__':

    print(shopify.productVariant)