import asyncio
import json
from typing import List

import httpx
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://www.realtor.com/rentals",
    "Alt-Used": "www.realtor.com",
    "Connection": "keep-alive",
    "Cookie": 'newPath=Astoria_NY; __vst=53bb0831-28b7-4265-aae3-b3a68afce768; __bot=false; AMCV_8853394255142B6A0A4C98A4%40AdobeOrg=-1124106680%7CMCIDTS%7C20378%7CMCMID%7C05067385349617451875576096832799666454%7CMCAID%7CNONE%7CMCOPTOUT-1760619683s%7CNONE%7CvVersion%7C5.2.0; __split=32; __rdc_id=rdc-id-6a7185fe-b3ba-40c9-b3cf-d2936b23e0a2; G_ENABLED_IDPS=google; kampyleUserSession=1760612463772; kampyleSessionPageCounter=4; kampyleUserSessionsCount=65; g_state={"i_p":1761157620921,"i_l":3,"i_ll":1760612485094,"i_b":"0HZbY83HfuZ8TMXFVBKLC4DA4bGSHcZSRuI7J14FGw0"}; split=n; split_tcv=151; _lr_env_src_ats=false; AWSALBTG=itjxJSL2LpYtmaIwaxzcInz1gEv4gUEBplyrjKmGrI2eu6Kw0nlkPTysrCZtg41hpM+6i85+4BqVi68wuRhGEozal2e47XQiYXXPnM7HqGyuuuTKK22+eIsGgM6LUK7K6JUDOhWlNwvivCi5DesofuBiQ/atsj3hz9u2eR6UOjcj; AWSALBTGCORS=itjxJSL2LpYtmaIwaxzcInz1gEv4gUEBplyrjKmGrI2eu6Kw0nlkPTysrCZtg41hpM+6i85+4BqVi68wuRhGEozal2e47XQiYXXPnM7HqGyuuuTKK22+eIsGgM6LUK7K6JUDOhWlNwvivCi5DesofuBiQ/atsj3hz9u2eR6UOjcj; AWSALB=SYAXepe8l3JawPqZeNVNPDjbKsdP8XP6AtE7f5Xhy8sI7Ue0XNeiFOxqiRC/1WIvpJn9ZkNxbRnFArSUwSnjoyaZDs1IHb9dLhqo8ssK4AiShQzfwaPhkv363SfV; AWSALBCORS=SYAXepe8l3JawPqZeNVNPDjbKsdP8XP6AtE7f5Xhy8sI7Ue0XNeiFOxqiRC/1WIvpJn9ZkNxbRnFArSUwSnjoyaZDs1IHb9dLhqo8ssK4AiShQzfwaPhkv363SfV; KP_UIDz-ssn=0esccldB0hkLg8sHOWwznKgam0VpcN0BoQPKy5U7FwPrPWEY45r9GXK60ZcSBJnkrP5tLvOa6Fk4mTBUJM0ZmNA38xnuL7FGJsKGAaVKwt9oLaXj7yUnArvnUZrWT2fntUBCcuTJbqs4SizCvN552hQEORNUra8lGLKBG28vlgu4IUL; KP_UIDz=0esccldB0hkLg8sHOWwznKgam0VpcN0BoQPKy5U7FwPrPWEY45r9GXK60ZcSBJnkrP5tLvOa6Fk4mTBUJM0ZmNA38xnuL7FGJsKGAaVKwt9oLaXj7yUnArvnUZrWT2fntUBCcuTJbqs4SizCvN552hQEORNUra8lGLKBG28vlgu4IUL; _lr_geo_location_state=NY; _lr_geo_location=US; ldp-property-details=true; ldp-home-value=true; ldp-environmental-risk=true; ldp-monthly-payment=false; ldp-open-houses=false; ldp-property-history=true; ldp-neighborhood=true; kampylePageLoadedTimestamp=1760560468064; __ssn=09454212-6102-4a04-8fdb-73ad07352823; __ssnstarttime=1760108071; AMCVS_8853394255142B6A0A4C98A4%40AdobeOrg=1; criteria=sprefix%3D%252Fnewhomecommunities%26area_type%3Dcity%26city%3DAstoria%26pg%3D1%26state_code%3DNY%26state_id%3DNY%26loc%3DAstoria%252C%2520NY%26locSlug%3DAstoria_NY%26county_fips%3D36081%26county_fips_multi%3D36081-36061; srchID=e87c9126320c4879b6c95db7530a4915; isRVLExists=true; _lr_retry_request=true; kampyleUserPercentile=26.11785357484123',
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
    # "TE": "trailers",
}
url = "https://www.realtor.com/apartments/Astoria_NY"
# url = "https://www.realtor.com/realestateandhomes-search/11103"


class RDC:
    def __init__(self, headers):
        self.session = httpx.AsyncClient(headers=headers)

    def parse():
        pass

    async def scrape(self, url):
        response = await self.session.get(url)
        self.html = response.text
        return self

    def getHTML(self, url):
        # options = Options()
        # options.add_argument("--headless=new")
        # driver = webdriver.Chrome(options=options)
        # driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": headers})

        # # Scrape url and extract html with soup
        # driver.get(url)

        # soup = BeautifulSoup(driver.page_source, "lxml")
        # self.soup = soup

        # driver.quit()
        # return self
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            context.set_extra_http_headers(headers)
            page = context.new_page()
            page.goto(url)
            html = page.content()
            browser.close()

        return self


if __name__ == "__main__":
    rdc = RDC(headers)
    # asyncio.run(rdc.scrape(url))
    rdc.getHTML(url)
