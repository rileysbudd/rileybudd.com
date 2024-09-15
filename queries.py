from types import SimpleNamespace

shopify_gql = SimpleNamespace(**{
    'variants_100':
    """
        query {
            productVariants(first: 100) {
                nodes {
                    id
                    sku
                    title
                    image {
                        url
                    }
                    price
                    compareAtPrice
                    product{
                        id
                    }
                    availableForSale
                }
                pageInfo {
                    hasPreviousPage
                    hasNextPage
                    startCursor
                    endCursor
                }
            }
        }
    """,

    # https://shopify.dev/docs/api/admin-graphql/2024-07/objects/Product#fields
    'products_100':
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
                    }
                    
                    
                                        
                    isGiftCard
                    hasOnlyDefaultVariant
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
                            }
                        }
                    variants(first: 100) {
                        nodes {
                            id
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
    """,

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
                    }
    
    
    
                    isGiftCard
                    hasOnlyDefaultVariant
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

    print(shopify_gql.products_100)