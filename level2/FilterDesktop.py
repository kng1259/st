# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class FilterDesktop(unittest.TestCase):
    def __init__(self, method_name, data, fields):
        super(FilterDesktop, self).__init__(method_name)
        self.data = data
        self.fields = fields

    def setUp(self):
        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test(self):
        driver = self.driver
        data = self.data
        fields = self.fields
        arrays = list(data.keys())[2:7]
        driver.get(fields['url'])
        if data['price_min']:
            driver.find_element_by_xpath(fields['price_min_xpath']).clear()
            driver.find_element_by_xpath(fields['price_min_xpath']).send_keys(str(data['price_min']))
        if data['price_max']:
            driver.find_element_by_xpath(fields['price_max_xpath']).clear()
            driver.find_element_by_xpath(fields['price_max_xpath']).send_keys(str(data['price_max']))
        for i in range(1, len(arrays) + 1):
            num = str(i if i < 3 else i + 1)
            for j in data[arrays[i - 1]]:
                res = "" if j == 1 else f"[{str(j)}]"
                driver.find_element_by_xpath(f"//div[@id='mz-filter-panel-0-{num}']/div/div{res}/div/label").click()
        if data['search']:
            driver.find_element_by_xpath(fields['search_xpath']).clear()
            driver.find_element_by_xpath(fields['search_xpath']).send_keys(str(data['search']))
            driver.find_element_by_xpath(fields['search_xpath']).send_keys(Keys.ENTER)
        time.sleep(4)
        if data['is_empty']:
            self.assertEqual("There are no products to list in this category.", driver.find_element_by_xpath("//div[@id='entry_212408']/p").text)
        else:
            self.assertEqual(data['res'], driver.find_element_by_xpath("//div[@id='entry_212409']/div/div[2]").text)
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    from helper import run_tests
    run_tests(FilterDesktop)