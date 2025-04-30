# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class ChangePassword(unittest.TestCase):
    def __init__(self, method_name, data, fields):
        super(ChangePassword, self).__init__(method_name)
        self.data = data
        self.fields = fields

    def login(self):
        driver = self.driver
        data = self.data
        fields = self.fields
        driver.get(fields['url'])
        driver.find_element_by_id(fields['login_email_id']).clear()
        driver.find_element_by_id(fields['login_email_id']).send_keys(data['email'])
        driver.find_element_by_id(fields['login_password_id']).clear()
        driver.find_element_by_id(fields['login_password_id']).send_keys(data['password'])
        driver.find_element_by_xpath(fields['login_button_xpath']).click()

    def setUp(self):
        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.login()
    
    def test(self):
        driver = self.driver
        data = self.data
        fields = self.fields
        time.sleep(1)
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/password")
        driver.find_element_by_id(fields['password_id']).clear()
        driver.find_element_by_id(fields['password_id']).send_keys(data['new_password'])
        driver.find_element_by_id(fields['confirm_id']).clear()
        driver.find_element_by_id(fields['confirm_id']).send_keys(data['confirm_password'])
        driver.find_element_by_xpath(fields['continue_xpath']).click()
        self.assertEqual(data['result'], driver.find_element_by_xpath(data['result_xpath']).text)

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
    run_tests(ChangePassword)