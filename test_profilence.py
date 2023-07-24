from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import unittest
import requests


class TestProfilenceSite(unittest.TestCase):

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

    @unittest.skip("skip")
    def test_navbar_links(self):
        """test that navbar link status codes return 200"""

        driver = self.driver
        driver.get("https://www.profilence.com/")
        nav = driver.find_element(By.CLASS_NAME, 'z-10')  # find navbar
        link_elements = nav.find_elements(By.TAG_NAME, 'a')
        links = [elem.get_attribute('href') for elem in link_elements]  # get all links to a list
        for item in links:
            status_code = requests.head(item).status_code  # get status code of link
            self.assertEqual(200, status_code,
                             msg=f"{item} returned {status_code} instead of 200")

    @unittest.skip("skip")
    def test_404_page(self):
        """test that 404 page has title and that page has link to at least home page"""

        driver = self.driver
        driver.get("https://www.profilence.com/notvalidurl")
        self.assertIn('404', driver.title)  # check if 404 in title
        # check that page infact returns the 404 code
        self.assertEqual(404, requests.head("https://www.profilence.com/notvalidurl").status_code)
        nav = driver.find_element(By.CLASS_NAME, 'z-10')
        link_elements = nav.find_elements(By.TAG_NAME, 'a')
        links = [elem.get_attribute('href') for elem in link_elements]

        # check that 404 page navbar has link to home page
        self.assertIn('https://www.profilence.com/', links)

    def test_footer_address_and_contact(self):
        """test the company address and link to email in footer"""

        driver = self.driver
        driver.get("https://www.profilence.com/")
        footer = driver.find_element(By.TAG_NAME, 'footer')  # find footer element
        profilence = footer.find_element(By.TAG_NAME, 'h2')  # profilence header
        self.assertEqual('Profilence Oy', profilence.get_attribute('innerHTML'))

        paragraphs = footer.find_elements(By.TAG_NAME, 'p')  # find all p elements in footer
        # check that the address is correct
        address = paragraphs[0].get_attribute('innerHTML')  # address part of footer
        self.assertIn('Elektroniikkatie 8', address)
        self.assertIn('90590 Oulu', address)
        self.assertIn('Finland', address)

        # check that the email link is correct
        contact = paragraphs[1].get_attribute('innerHTML')
        self.assertIn('mailto:contact@profilence.com', contact)
        self.assertIn('@profilence.com', contact)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
