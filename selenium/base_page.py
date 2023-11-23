# pages\\base_pages



import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from Utilities.customLogger import LogGen

logger = LogGen.loggen()

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def get_page_title(self):
        return self.driver.title
    
    def find_element_with_retry(self, by_locator, max_attempts=3, wait_time=10):
        attempts = 0
        while attempts < max_attempts:
            try:
                element = WebDriverWait(self.driver, wait_time).until(EC.element_to_be_clickable(by_locator))
                return element
            except (TimeoutException, StaleElementReferenceException):
                attempts += 1
        logger.error(f'Element with {by_locator} not found after {max_attempts} attempts.')
        raise NoSuchElementException(f'Element with {by_locator} not found after {max_attempts} attempts.')
    
    def click_button(self, by_locator):
        element = self.find_element_with_retry(by_locator)
        if element.is_displayed() or element.is_enabled():
            element.click()
        else:
            print('button not found')
    
    def do_send_keys(self, by_locator, text):
        element = self.find_element_with_retry(by_locator)
        if element.is_enabled() or element.is_displayed():
            element.send_keys(text)
        else:
            element = self.wait_for_element(by_locator)
            element.send_keys(text)
    
    def get_element_inner_text(self, by_locator):
        element = self.find_element_with_retry(by_locator)
        return element.text
    
    def is_enabled(self, by_locator):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(by_locator))
            if element:
                return True
            else:
                return False
        except TimeoutException:
            logger.info(f'Element with {by_locator} is not enabled.')
            return False

    def is_element_displayed(self, by_locator):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
            if element:
                return True
        except TimeoutException:
            return False

        return False
    
    def select_value_from_dropdown(self, dropdownelement, option):
        dropdownelement = self.find_element_with_retry(dropdownelement)
        dropdown = Select(dropdownelement)
        dropdown.select_by_value(option)
    
    def set_attribute_element(self, by_locator, attribute_value):
        element = self.find_element_with_retry(by_locator)
        self.driver.execute_script(f"arguments[0].setAttribute('value', '{attribute_value}')", element)
    
    def do_js_click(self, by_locator):
        element = WebDriverWait(self.driver, 25).until(EC.visibility_of_element_located(by_locator))
        if element.is_displayed() | element.is_enabled():
            self.driver.execute_script("arguments[0].click();", element)
        else:
            print("Button not found")
        
    def do_Selenium_click(self, by_locator):
        element = WebDriverWait(self.driver, 25).until(EC.visibility_of_element_located(by_locator))
        if element.is_displayed() | element.is_enabled():
            element.click()
        else:
            print("Button not found")
    
    def do_send_keys_by_actions(self, by_locator, value):
        actions = ActionChains(self.driver)
        element = self.find_element_with_retry(by_locator)
        actions.move_to_element(element).click().send_keys(value).perform()
    
    def get_todays_date(self):
        return time.strftime("%d/%m/%Y")
    
    def element_hover(self, by_locator):
        element = self.find_element_with_retry(by_locator)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
    
    def get_table_data_from_table(self, by_locator):
        table_element = self.find_element_with_retry(by_locator)
        headers = [header.text for header in table_element.find_elements(By.XPATH, ".//thead/tr/th")]
        table_rows = table_element.find_elements(By.XPATH, ".//tbody/tr")
        table_data = []
        for row in table_rows:
            row_data = {}
            cells = row.find_elements(By.TAG_NAME, 'td')
            for index, cell in enumerate(cells):
                row_data[headers[index]] = cell.text
            table_data.append(row_data)
        return table_data