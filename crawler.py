import argparse
from ShopeeCrawler import ProductCrawler, RatingCrawler

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Shopee Crawler')
    parser.add_argument('--crawl', dest='type_crawler', type=str, default='product',
                        help='There are 2 types crawler is "product" and "rating", default is "product"')
    parser.add_argument('--product_limit', dest='product_limit', type=int, default=200,
                        help='Limit number of product to crawl, must is "integer", default is 200')
    parser.add_argument('--rating_limit', dest='rating_limit', type=int, default=30,
                        help='Limit number of user rating to crawl, must is "integer", default is 30')
    parser.add_argument('--index', dest='category_to_crawl', default=None,
                        help='Category to crawl from 0 to 24, must is "integer" or "list", default is "None"')
    args = parser.parse_args()

    if isinstance(args.product_limit, int):
        product_limit = args.product_limit
    else:
        raise Exception('Product limit must be integer')

    if isinstance(args.rating_limit, int):
        rating_limit = args.rating_limit
    else:
        raise Exception('Rating limit must be integer')

    if (isinstance(args.category_to_crawl, int)) or (isinstance(eval(args.category_to_crawl), list)):
        index = eval(args.category_to_crawl)
    else:
        raise Exception('Index of categorical must be integer')

    if args.type_crawler == 'product' or args.type_crawler == 'rating':
        type_crawler = args.type_crawler
    else:
        raise Exception('Only 2 type of crawler is "product" or "rating" !!!')

    print('Setting {} bot crawler'.format(type_crawler))
    print('Setting crawl {} product'.format(str(product_limit)))

    if type_crawler == 'product':
        if index is None:
            print('Setting crawl all category')
        elif isinstance(index, list):
            print('Setting crawl category {}'.format(index))
        elif type(index) == int:
            print('Setting crawl category {}'.format(index))

        prod_crawler = ProductCrawler()
        prod_crawler.crawl(product_limit, index)

    elif type_crawler == 'rating':
        if index is None:
            print('Setting crawl all category')
        elif isinstance(index, list):
            print('Setting crawl crawl category {}'.format(index))
        elif type(index) == int:
            print('Setting crawl {} category'.format(index))

        print('Setting crawl {} rating per each product'.format(str(rating_limit)))

        rating_crawler = RatingCrawler()
        rating_crawler.crawl(product_limit, rating_limit, index)
