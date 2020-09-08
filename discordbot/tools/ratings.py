import selenium
from selenium import webdriver
import selenium.webdriver.chrome.service
import selenium.webdriver.chrome.options


class CharacterRater:
    def __init__(self):
        """
        Need a class to keep the driver going and to not ave to spin it all up every time we want to make a single web
        request, ok two web requests per character
        """

        # Yes we apparently need to run this without sandboxing OR a head to the connection for this to function properly
        # This means that we need to also make sure that the docker container isn't using the root user when we deploy
        chrome_options = selenium.webdriver.chrome.options.Options()
        chrome_options.binary_location = '/usr/bin/chromium'
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        self.chrome_driver = selenium.webdriver.Chrome(options=chrome_options, executable_path='/usr/bin/chromedriver')

        # self.chrome_service = selenium.webdriver.chrome.service.Service('/usr/bin/chromedriver')
        # self.chrome_service.start()

    def get_character_ratings(self, character_name, character_spec):
        """

        :param self:
        :param character_name:
        :return:
        """
        spec_addition = {"heal": "&metric=hps"}.get(character_spec, "")
        self.chrome_driver.get(
            f"https://classic.warcraftlogs.com/character/us/atiesh/{character_name}#zone=1002&partition=2{spec_addition}")
        bwl_perf_avg = self.chrome_driver.find_element_by_css_selector(".best-perf-avg>b").text
        aq_tab = self.chrome_driver.find_element_by_id("partitions-tab-3")
        aq_tab.click()
        aq_perf_avg = self.chrome_driver.find_element_by_css_selector(".best-perf-avg>b").text
        return {"bwl": bwl_perf_avg, "aq40": aq_perf_avg}
