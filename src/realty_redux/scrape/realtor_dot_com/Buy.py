import requests
from typing import Self

import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome


class Buy:
    def __init__(self, driver: Chrome = None):
        self.driver: Chrome

        if not driver:
            self.get_driver()
        else:
            self.driver = driver

    def __call__(self, url: str):
        self.get_data(url)
        return self.data

    def get_driver(self) -> Self:
        self.driver = uc.Chrome(headless=False, use_subprocess=False)
        return self

    def get_data(self, url: str) -> Self:
        self.driver.get(url)
        # Adapted https://stackoverflow.com/questions/62262261/how-to-get-request-headers-in-selenium
        user_agent_script = """
            var userAgent = navigator.userAgent;
            return userAgent;
        """
        user_agent = self.driver.execute_script(user_agent_script)
        headers = {"User-Agent": user_agent}
        pass

if __name__ == "__main__":
    Buy()("https://www.scrapethissite.com/")
    pass
