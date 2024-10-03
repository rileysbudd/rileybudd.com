from types import SimpleNamespace

shopify_gql = SimpleNamespace(**{
    'store_info':
    """
        query {
            shop{
                primaryDomain {
                    url
                }
                currencyCode
                email
            }
        }
    """,

    # https://shopify.dev/docs/api/admin-graphql/2024-07/objects/Product#fields
    'products_variants_100x100':
    """
        {
            products(first: 100) {
                nodes {
                    id
                    title
                    description
                    descriptionHtml
                    onlineStoreUrl
                    featuredMedia {
                        id
                        mediaContentType
                        preview{
                            image{
                                url
                            }
                        }
                    }
                    vendor
                    isGiftCard
                    hasOnlyDefaultVariant
                    productType
                    options {
                        name
                    }
                    status
                    seo {
                        title
                        description
                    }
                    media(first: 20) {
                        nodes {
                            id
                                mediaContentType
                                preview{
                                    image{
                                        url
                                    }
                                }
                            }
                        }
                    variants(first: 100) {
                        nodes {
                            id
                            sku
                            title
                            image {
                                url
                            }
                            price
                            compareAtPrice
                            availableForSale
                            inventoryItem {
                                unitCost{
                                    amount
                                    currencyCode
                                }
                            }
                            selectedOptions{
                                name
                                value
                            }
                        }
                        pageInfo {
                            hasPreviousPage
                            hasNextPage
                            startCursor
                            endCursor
                        }
                    }
                }
                pageInfo {
                    hasPreviousPage
                    hasNextPage
                    startCursor
                    endCursor
                }
            }
        }
    """
})

if __name__ == '__main__':

    print(shopify_gql.product_variants_100x100)