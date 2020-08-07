import os
import pandas as pd
from contextlib import contextmanager

from BaseCrawler.BaseCrawler import BaseCrawler
from utils.logger import get_logger
from utils.utils import scroll_down_and_wait

BASE_PATH_CRAWLER = os.path.dirname(os.path.abspath(__file__))
LOG_PATH_CRAWLER = os.path.join(BASE_PATH_CRAWLER, 'log_dir')


class ProductCrawler(BaseCrawler):
    def __init__(self):
        '''
        This Class Inherited from BaseCrawler and add new method
        '''
        BaseCrawler.__init__(self)
        self.logger = get_logger(LOG_PATH_CRAWLER, __class__.__name__)
        self.get_site()
        self.logger.info('Bot get site shopee succeeded...')
        self.categorical_url = self.get_categorical_url()

    @contextmanager
    def move_from_page_to_page(self):
        '''
        Due to after crawl all product in page, we need to get back the original page for moving next,
        this contextmanager help to move back and jump into next page
        :return:
        '''
        try:
            current_url = self.driver.current_url
            list_product_url = self.get_product_url()
            yield list_product_url
        finally:
            self.driver.get(current_url)
            self.driver = scroll_down_and_wait(self.driver)
            self.driver.find_element_by_xpath(
                "//button[@class='shopee-icon-button shopee-icon-button--right ']").click()

    def crawl_single_category_prod(self, ind, limit_prod):
        '''
        This method use to crawl single product category
        :param ind: Index of product category need to crawl
        :param limit_prod: Quantities of product we need to crawl
        :return: csv file contain info of product crawled
        '''
        product_all = list()
        label = self.index_category.get(ind)
        self.logger.info('Bot started getting product info from {}'.format(label))
        self.to_best_sale(self.categorical_url[ind])
        while True:
            with self.move_from_page_to_page() as list_product_url:
                self.logger.info('Shopee returned {} url of product'.format(len(list_product_url)))
                if len(list_product_url) < 30:
                    self.driver.refresh()
                    self.driver = scroll_down_and_wait(self.driver)
                else:
                    for product_url in list_product_url:
                        self.logger.info('Bot started move into each product')
                        self.to_product_site(product_url)
                        if 'event3' in self.driver.current_url:
                            self.logger.info('Advertising block encounter, move to next url')
                            continue
                        else:
                            self.logger.info('Bot parsed info of product')
                            product_info = self.parse_info_product(label)
                            product_all.append(product_info)
            self.logger.info('Bot parsed {} product from list'.format(len(product_all)))
            if len(product_all) >= limit_prod:
                df = pd.DataFrame(product_all)
                save_path = os.path.join(BASE_PATH_CRAWLER, 'data_collected/{}_prod.csv'.format(label))
                df.to_csv(save_path, index=False)
                break

    def crawl_all_category_prod(self, limit_prod):
        '''
        This method to crawl product of all category
        :param limit_prod:
        :return: csv files contain product info of all category
        '''
        self.logger.info('Bot not found index, collect product info from all categorical')
        for ind, url_item in enumerate(self.categorical_url):
            product_all = list()
            label = self.index_category.get(ind)
            self.logger.info('Bot started get product info from {}'.format(label))
            self.to_best_sale(url_item)
            while True:
                with self.move_from_page_to_page() as list_product_url:
                    self.logger.info('Shopee returned {} url of product'.format(len(list_product_url)))
                    if len(list_product_url) < 30:
                        self.driver.refresh()
                        self.driver = scroll_down_and_wait(self.driver)
                    else:
                        for product_url in list_product_url:
                            self.logger.info('Bot started move into each product')
                            self.to_product_site(product_url)
                            if 'event3' in self.driver.current_url:
                                self.logger.info('Advertising block encountered, moving to next url')
                                continue
                            else:
                                self.logger.info('Bot parsed info of product')
                                product_info = self.parse_info_product(label)
                                product_all.append(product_info)
                self.logger.info('Bot parsed {} product from list'.format(len(product_all)))
                if len(product_all) >= limit_prod:
                    save_path = os.path.join(BASE_PATH_CRAWLER, 'data_collected/{}_prod.csv'.format(label))
                    df = pd.DataFrame(product_all)
                    df.to_csv(save_path, index=False)
                    break

    def crawl(self, limit, indx=None):
        '''
        Execute the Crawler, if we not input index, Crawler will crawl all category
        :param limit: Quantities of product we need to crawl
        :param indx: Index of product we need to crawl
        :return:
        '''
        if indx is None:
            self.crawl_all_category_prod(limit_prod=limit)
            self.driver.close()
        elif isinstance(indx, list):
            for ite in indx:
                self.crawl_single_category_prod(ind=ite, limit_prod=limit)
            self.driver.close()
        else:
            self.crawl_single_category_prod(ind=0, limit_prod=limit)
            self.driver.close()


class RatingCrawler(ProductCrawler):
    def __init__(self):
        '''
        This Class inherited from ProductCrawler but change method to crawl user rating and comment instead of crawl product info
        '''
        ProductCrawler.__init__(self)
        self.logger = get_logger(LOG_PATH_CRAWLER, __class__.__name__)

    def crawl_single_category_rating(self, ind, limit_prod, limit_user):
        '''
        This method to crawl a single product category
        :param ind: Index of category in product
        :param limit_prod: Quantities of product in each category
        :param limit_user: Quantities of user rating in each product
        :return: csv file contain user rating
        '''
        count_prod = 0
        user_rating_all = pd.DataFrame([], columns=['username', 'rating', 'comment', 'sp'])
        label = self.index_category.get(ind)
        self.logger.info('Bot start get rating from {}'.format(label))
        self.to_best_sale(self.categorical_url[ind])
        while True:
            with self.move_from_page_to_page() as list_product_url:
                self.logger.info('Shopee returned {} url of product'.format(len(list_product_url)))
                if len(list_product_url) < 30:
                    self.driver.refresh()
                    self.driver = scroll_down_and_wait(self.driver)
                else:
                    for product_url in list_product_url:
                        self.logger.info('Bot started get into each product')
                        self.to_product_site(product_url)
                        if 'event3' in self.driver.current_url:
                            self.logger.info('Advertising block encountered, moving to next url')
                            continue
                        else:
                            self.logger.info('Bot parsed rating of user')
                            user_rating_item = self.get_user_rating(limit_user)
                            user_rating_all = user_rating_all.append(user_rating_item, sort=False)
                            user_rating_all = user_rating_all.drop_duplicates().reset_index(drop=True)
                            self.logger.info('Bot collected {} rating of user'.format(user_rating_all.shape[0]))
                            count_prod += 1
            self.logger.info('Bot parsed {} product from list'.format(count_prod))
            if count_prod >= limit_prod:
                save_path = os.path.join(BASE_PATH_CRAWLER, 'data_collected/{}_rating.csv'.format(label))
                user_rating_all.to_csv(save_path, index=False)
                break

    def crawl_all_category_rating(self, limit_prod, limit_user):
        '''
        This method to crawl all product category
        :param limit_prod: Quantities of product for each category
        :param limit_user: Quantities of user rating for each product
        :return: csv files contain user rating
        '''
        self.logger.info('Bot not found index, collect product info from all categorical')
        for ind, url_item in enumerate(self.categorical_url):
            count_prod = 0
            user_rating_all = pd.DataFrame([], columns=['username', 'rating', 'comment', 'sp'])
            label = self.index_category.get(ind)
            self.logger.info('Bot started geting product info from {}'.format(label))
            self.to_best_sale(url_item)
            while True:
                with self.move_from_page_to_page() as list_product_url:
                    self.logger.info('Shopee returned {} url of product'.format(len(list_product_url)))
                    if len(list_product_url) < 30:
                        self.driver.refresh()
                        self.driver = scroll_down_and_wait(self.driver)
                    else:
                        for product_url in list_product_url:
                            self.logger.info('Bot started get into each product')
                            self.to_product_site(product_url)
                            if 'event3' in self.driver.current_url:
                                self.logger.info('Advertising block encountered, moving to next url')
                                continue
                            else:
                                self.logger.info('Bot parsed rating of user')
                                user_rating_item = self.get_user_rating(limit_user)
                                user_rating_all = user_rating_all.append(user_rating_item, sort=False)
                                user_rating_all = user_rating_all.drop_duplicates().reset_index(drop=True)
                                self.logger.info(
                                    'Bot collected {} rating of user'.format(user_rating_all.shape[0]))
                                count_prod += 1
                self.logger.info('Bot parsed {} product from list'.format(count_prod))
                if count_prod >= limit_prod:
                    save_path = os.path.join(BASE_PATH_CRAWLER, 'data_collected/{}_rating.csv'.format(label))
                    user_rating_all.to_csv(save_path, index=False)
                    break

    def crawl(self, limit, limit_rating, indx=None):
        '''
        Execute crawler to crawl user rating, if we not input the index, Crawler will crawll all category
        :param limit: Quantities product for each category we want to crawl
        :param limit_rating: Quantities of user rating for each product we want to crawl
        :param indx: Index of category
        :return:
        '''
        if indx is None:
            self.crawl_all_category_rating(limit_prod=limit, limit_user=limit_rating)
            self.driver.close()
        elif isinstance(indx, list):
            for ite in indx:
                self.crawl_single_category_rating(ind=ite, limit_prod=limit, limit_user=limit_rating)
            self.driver.close()
        else:
            self.crawl_single_category_rating(ind=0, limit_prod=limit, limit_user=limit_rating)
            self.driver.close()
