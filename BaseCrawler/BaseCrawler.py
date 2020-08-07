import time

import pandas as pd
import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.index_category import index_category
from utils.utils import scroll_down_and_wait, get_link_product, get_price, get_rating_shop, get_image_url, \
    get_other_info_shop


class BaseCrawler:

    def __init__(self):
        '''
        Init the browser and get category label to crawl
        '''
        self.driver = webdriver.Firefox()
        self.index_category = index_category

    def get_site(self):
        '''
        Go to shopee.vn website, close the popup and maximize the window of browser
        :return: None
        '''
        self.driver.get("https://shopee.vn/")
        time.sleep(random.randint(3, 6))
        popup_close_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'shopee-popup__close-btn')]")))
        if popup_close_button:
            popup_close_button.click()
        self.driver.maximize_window()

    def get_categorical_url(self):
        '''
        Get the url link of categorical in shopee website
        :return: list of links
        '''
        categoty_url = []
        category = self.driver.find_elements_by_class_name('home-category-list__group')
        for sub_item in category:
            categoty_url.extend([ssitem.get_attribute('href') for ssitem in
                                 sub_item.find_elements_by_class_name('home-category-list__category-grid')])
        return categoty_url[:-1]  ## Shopee only return 23 item, last item is None

    def to_best_sale(self, url_item):
        '''
        To get the common product with high rating and sale, we sort product by sale
        :param url_item:
        :return: None
        '''
        self.driver.get(url_item)
        self.driver = scroll_down_and_wait(self.driver)
        self.driver.find_elements_by_xpath("//*[contains(text(), 'Bán chạy')]")[0].click()
        time.sleep(random.randint(3, 8))
        self.driver = scroll_down_and_wait(self.driver)

    def get_product_url(self):
        '''
        Get product url each page
        :return: None
        '''
        self.driver = scroll_down_and_wait(self.driver)
        time.sleep(random.randint(3, 8))
        _, product_url = get_link_product(self.driver)
        return product_url

    def to_product_site(self, product_url):
        '''
        Go to each product site for get information of product and user rating and comment
        :param product_url:
        :return:
        '''
        self.driver.get(product_url)
        time.sleep(random.randint(3, 8))
        self.driver = scroll_down_and_wait(self.driver)
        try:
            self.driver.find_element_by_xpath(
                "//button[@class='btn btn-solid-primary btn--m btn--inline shopee-alert-popup__btn']").click()
            print('Confirmed 18+')
        except NoSuchElementException:
            pass

    def parse_info_product(self, label):
        '''
        Parse html from page and filter information we need
        :param label:
        :return: dict contain info of product we want to get
        '''
        info_dict = {}
        product_span = self.driver.find_elements_by_class_name("qaNIZv")
        if len(product_span) > 0:

            info_dict.update({'Content': product_span[0].text.split('\n')[-1], 'Category': label})

            for attr in self.driver.find_elements_by_class_name("kIo6pj"):
                info_dict.update({attr.text.split('\n')[0]: '-'.join(attr.text.split('\n')[1:])})

            self.driver = get_price(self.driver, info_dict)
            self.driver = get_rating_shop(self.driver, info_dict)
            self.driver = get_image_url(self.driver, info_dict)
            self.driver = get_other_info_shop(self.driver, info_dict)
        else:
            pass
        return info_dict

    def parse_user_rating(self, list_author, list_rating, list_comment):
        '''
        Parse html from page and get info of user rating and comment
        :param list_author:
        :param list_rating:
        :param list_comment:
        :return: dict contain user rating and comment
        '''
        list_user_info = []
        product_span = self.driver.find_elements_by_class_name("qaNIZv")
        if len(product_span) > 0:
            product = product_span[0].text.split('\n')[-1]
            for idx, author in enumerate(list_author):
                user_name = author.text
                stars = list_rating[idx].get_attribute('innerHTML').split().count('enable-background="new')
                comment = list_comment[idx].text
                list_user_info.append({'username': user_name, 'rating': stars, 'comment': comment, 'sp': product})
        return list_user_info

    def get_user_rating(self, limit_user):
        '''
        Due to some product have a thousands user comment and rating so we need to limit
        the quantities of info we crawled
        :param limit_user:
        :return: Dataframe info which user rating and comment
        '''
        user_rating_item = pd.DataFrame([], columns=['username', 'rating', 'comment', 'sp'])
        user_rating_old = pd.DataFrame([], columns=['username', 'rating', 'comment', 'sp'])
        user_rating = pd.DataFrame()
        try:
            while True:
                list_author = self.driver.find_elements_by_class_name('shopee-product-rating__author-name')
                list_rating = self.driver.find_elements_by_class_name('shopee-product-rating__rating')
                list_comment = self.driver.find_elements_by_class_name('shopee-product-rating__content')
                list_user_info = self.parse_user_rating(list_author, list_rating, list_comment)
                if len(list_user_info) == 0:
                    break
                else:
                    if user_rating_old.equals(user_rating):
                        break
                    else:
                        user_rating_old = user_rating.copy()
                        user_rating = pd.DataFrame(list_user_info)
                        user_rating_item = user_rating_item.append(user_rating)
                        user_rating_item = user_rating_item.drop_duplicates().reset_index(drop=True)
                        self.driver.find_element_by_xpath(
                            "//button[@class='shopee-icon-button shopee-icon-button--right ']").click()
                        time.sleep(3)
                        if user_rating_item.shape[0] > limit_user:
                            break
        except NoSuchElementException:
            pass
        return user_rating_item
