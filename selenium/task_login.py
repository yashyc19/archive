from Tasks.task_base import BaseTask
from Pages.login_page import LoginPage
from Config.Config import DevData
from Utilities.customLogger import LogGen

from time import sleep


class LoginTask(BaseTask):
    logger = LogGen.loggen()

    def __init__(self):
        super().__init__()

    def task_loginpage(self, username, password):
        self.logger.info('========= TASK - login =========')
        loginpage = LoginPage(self.driver)
        loginpage.do_login(username, password)
        sleep(3)
        title = loginpage.get_page_title()
        if title == DevData.HOMEPAGE_TITLE:
            self.logger.info('========= TASK successful =========')
        else:
            self.logger.info('========= TASK failed =========')
        self.close_driver()
