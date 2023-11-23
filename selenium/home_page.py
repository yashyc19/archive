# Pages\\home_page

from time import sleep


from selenium.webdriver.common.by import By
from Pages.base_page import BasePage
from Utilities.customLogger import LogGen

class HomePage(BasePage):
    logger = LogGen.loggen()

    Text_Login_User = (By.XPATH, '/html/body/div[1]/ng-include[1]/header/div[2]/div/div/ul/li[1]/div/a/span')
    Link_Login_Page = (By.XPATH, '/html/body/div[1]/header/div[2]/div/div/ul/li/a')
    Button_Dashboard = (By.XPATH, '//a[@data-ng-href="//services.gst.gov.in/services/auth/dashboard"]')
    Button_Services = (By.XPATH, '//*[@id="main"]/ul/li[2]/a')

    def __init__(self, driver):
        super().__init__(driver)
    
    def get_login_id(self):
        return self.get_element_inner_text(self.Text_Login_User)
    
    def goto_login(self):
        self.click_button(self.Link_Login_Page)

    def goto_dashboard(self):
        self.click_button(self.Button_Dashboard)
    
    def goto_services(self):
        self.click_button(self.Button_Services)

    def do_logout(self):
        Link_Profile = (By.XPATH, '/html/body/div[1]/ng-include[1]/header/div[2]/div/div/ul/li[1]/div/a')
        Link_Logout = (By.XPATH, '/html/body/div[1]/ng-include[1]/header/div[2]/div/div/ul/li[1]/div/ul/li[5]/a')

        self.goto_dashboard()
        sleep(5)
        self.click_button(Link_Profile)
        sleep(2)
        self.click_button(Link_Logout)
        sleep(2)
        