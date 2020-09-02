import os
import loguru
import selenium

from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.chrome import options

#import pandas as pd
from bs4 import BeautifulSoup



class CharacterRater:
    def __init__(self):
        """

        """
        selenium.webdriver.common.keys.Keys()
        chrome_options_handle = selenium.webdriver.chrome.options.Options()
        chrome_options_handle.add_argument("--headless")
        chrome_options_handle.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        self.request_driver = selenium.webdriver.Chrome(executable_path=os.path.abspath('/usr/local/bin/chromedriver'),chrome_options=chrome_options_handle)

    def get_character_ratings(self, character_name):
        """

        :param self:
        :param character_name:
        :return:
        """

        self.request_driver.get(f"https://classic.warcraftlogs.com/character/us/atiesh/{character_name}#zone=1002&partition=2")
        bwl_perf_avg = self.request_driver.find_element_by_css_selector(".best-perf-avg>b").text
        aq_tab = self.request_driver.find_element_by_id("partitions-tab-3")
        aq_tab.click()
        aq_perf_avg = self.request_driver.find_element_by_css_selector(".best-perf-avg>b").text
        return (bwl_perf_avg,aq_perf_avg)
