
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from Config.Config import DevData
from Utilities.customLogger import LogGen

logger = LogGen.loggen()


class BaseTask:
    # declare driver at class level
    driver = None
    
    def __init__(self):
        self.init_driver()

    @classmethod
    def init_driver(cls):
        logger.info(f'======Loading webdrivers for chrome======')
        options = Options()
        options.add_argument('start-maximized')
        prefs = {"download.default_directory": DevData.DOWNLOADS_FOLDER}
        options.add_experimental_option("prefs", prefs)
        # driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager(driver_version='115.0.5790.111').install()))
        BaseTask.driver = webdriver.Chrome(options=options)
        print('launching chromedriver from init_driver ...')
        # driver.get(TestData.HOME_URL)
        BaseTask.delete_cache(BaseTask.driver)  # Call delete_cache using the class name
        BaseTask.driver.delete_all_cookies()
        BaseTask.driver.get(DevData.HOME_URL)
        return BaseTask.driver
    
    @classmethod
    def delete_cache(cls, driver):
        driver.execute_script("window.open('')")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get('chrome://settings/clearBrowserData')
        cls.perform_actions(driver, Keys.TAB * 2 + Keys.DOWN * 4 + Keys.TAB * 5 + Keys.ENTER)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    @classmethod
    def perform_actions(cls, driver, keys):
        actions = ActionChains(driver)
        actions.send_keys(keys)
        time.sleep(2)
        print('Performing Actions!')
        actions.perform()
    
    @classmethod
    def close_driver(cls):
        logger.info(f'======Closing webdrivers for chrome======')
        BaseTask.driver.close()
        BaseTask.driver.quit()
        logger.info('closing chromedriver ...')

    