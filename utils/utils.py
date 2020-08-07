import time

import random
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def scroll_down_and_wait(driver):
    actions = ActionChains(driver)
    for _ in range(4):
        actions.send_keys(Keys.SPACE).perform()
        time.sleep(random.randint(3, 5))
    return driver


def scroll_up_and_wait(driver):
    actions = ActionChains(driver)
    for _ in range(2):
        actions.send_keys(Keys.PAGE_UP).perform()
        time.sleep(random.randint(3, 5))
    return driver


def get_link_product(driver):
    all_items = driver.find_elements_by_xpath('//a[@data-sqe="link"]')
    all_urls = []
    for item in all_items:
        url = item.get_attribute('href')
        all_urls.append(url)
    return driver, all_urls


def get_price(driver, info_dict):
    if len(driver.find_elements_by_class_name("_3_ISdg")) == 0:
        info_dict.update({'sale_price': driver.find_elements_by_class_name("_3n5NQx")[0].text})
        info_dict.update({'org_price': driver.find_elements_by_class_name("_3n5NQx")[0].text})
        info_dict.update({'discount': 0})
    else:
        info_dict.update({'org_price': driver.find_elements_by_class_name("_3_ISdg")[0].text})
        info_dict.update({'sale_price': driver.find_elements_by_class_name("_3n5NQx")[0].text})
        info_dict.update({'discount': driver.find_elements_by_class_name("MITExd")[0].text})
    return driver


def get_rating_shop(driver, info_dict):
    if len(driver.find_elements_by_class_name("_3Oj5_n")) == 0:
        info_dict.update({'star': 0})
        info_dict.update({'rating': 0})
    else:
        for i in driver.find_elements_by_class_name("_3Oj5_n"):
            info_dict.update({'star': driver.find_elements_by_class_name("_3Oj5_n")[0].text})
            info_dict.update({'rating': driver.find_elements_by_class_name("_3Oj5_n")[1].text})
    return driver


def get_image_url(driver, info_dict):
    try:
        my_property = driver.find_element_by_class_name('_3ZDC1p').find_element_by_xpath(
            "//div[@class='_2JMB9h _3XaILN']").value_of_css_property("background-image")
        info_dict.update({'img_url': re.split('[()]', my_property)[1]})
    except NoSuchElementException:
        info_dict.update({'img_url': ''})
    return driver


def get_other_info_shop(driver, info_dict):
    info_dict.update({'selled': driver.find_elements_by_class_name("_22sp0A")[0].text})
    info_dict.update({driver.find_elements_by_class_name("TuJk3S")[0].text.split('\n')[0]:
                          driver.find_elements_by_class_name("TuJk3S")[0].text.split('\n')[1]})
    info_dict.update({driver.find_elements_by_class_name("TuJk3S")[0].text.split('\n')[2]:
                          driver.find_elements_by_class_name("TuJk3S")[0].text.split('\n')[3]})
    info_dict.update({driver.find_elements_by_class_name("TuJk3S")[1].text.split('\n')[0]:
                          driver.find_elements_by_class_name("TuJk3S")[1].text.split('\n')[1]})
    info_dict.update({driver.find_elements_by_class_name("TuJk3S")[1].text.split('\n')[2]:
                          driver.find_elements_by_class_name("TuJk3S")[1].text.split('\n')[3]})
    info_dict.update({driver.find_elements_by_class_name("TuJk3S")[2].text.split('\n')[0]:
                          driver.find_elements_by_class_name("TuJk3S")[2].text.split('\n')[1]})
    info_dict.update({driver.find_elements_by_class_name("TuJk3S")[2].text.split('\n')[2]:
                          driver.find_elements_by_class_name("TuJk3S")[2].text.split('\n')[3]})
    return driver
