from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import unittest
import requests


class CheckGoogleTitle(unittest.TestCase):

    def setUp(self):
        self.options = Options()
        options = self.options
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_prefs = {}
        options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        self.driver = webdriver.Chrome(options=options)

    @unittest.skip()
    def test_navbar_links(self):
        """test that navbar link status codes return 200"""
        driver = self.driver
        driver.get("https://www.profilence.com/")
        nav = driver.find_element(By.CLASS_NAME, 'z-10')
        link_elements = nav.find_elements(By.TAG_NAME, 'a')
        links = [elem.get_attribute('href') for elem in link_elements]
        #status_codes = set([requests.head(item).status_code for item in links])
        for item in links:
            status_code = requests.head(item).status_code
            self.assertEqual(200, status_code,
                             msg=f"{item} returned {status_code} instead of 200")

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)

# driver_path = Path.cwd() / 'chromedriver.exe'
