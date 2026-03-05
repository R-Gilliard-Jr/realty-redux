import json
import time
from typing import Self

import undetected_chromedriver as uc
from selenium.webdriver import Chrome, ActionChains

from realty_redux.scrape.realtor_dot_com.java_script import parseCards


class Buy:
    def __init__(self, driver: Chrome = None):
        self.driver: Chrome
        self.x_scroll_amount: int = 100
        self.y_scroll_amount: int = 100

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
        time.sleep(1)
        # wait = WebDriverWait(self.driver, 10)
        # wait.until()
        actions = ActionChains(self.driver)
        # https://www.realtor.com/realestateandhomes-search/19121
        height = self.driver.execute_script(
            "var pageHeight = document.body.scrollHeight; return pageHeight"
        )
        current_y = 0
        while current_y < height:
            actions.scroll_by_amount(0, self.y_scroll_amount).perform()
            current_y += self.y_scroll_amount
            time.sleep(0.5)
        card_data = self.driver.execute_script(parseCards)
        card_data = json.loads(card_data)


if __name__ == "__main__":
    Buy()("https://www.realtor.com/realestateandhomes-search/19121")
    pass
