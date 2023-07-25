from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import unittest
import requests


class TestProfilenceSite(unittest.TestCase):

    def setUp(self):
        self.options = Options()
        options = self.options
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--log-level=3")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_prefs = {}
        options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        self.driver = webdriver.Chrome(service=Service("/chromedriver"), options=options)
        self.home = "https://www.profilence.com/"

    # @unittest.skip("skip")
    def test_navbar_status_codes(self):
        """test that request to navbar links return status code 200"""

        driver = self.driver
        driver.get(self.home)
        nav_links = driver.find_element(By.ID, 'header').find_elements(By.TAG_NAME, 'a')  # find navbar links
        links = [elem.get_attribute('href') for elem in nav_links]  # get all links to a list
        for item in links:
            status_code = requests.head(item).status_code  # get status code of link
            # print(f"{item}, {status_code}") # added mainly for some extra console output in jenkins
            self.assertEqual(200, status_code,
                             msg=f"{item} returned {status_code} instead of 200")

    # @unittest.skip("skip")
    def test_404_page(self):
        """test that 404 page has title and that page has link to at least home page"""

        driver = self.driver
        invalid_link = "https://www.profilence.com/notvalidurl"
        driver.get(invalid_link)
        self.assertIn('404', driver.title)
        # check that page returns the 404 code, might be useless to test but not 100% sure
        self.assertEqual(404, requests.head(invalid_link).status_code)
        nav_links = driver.find_element(By.ID, 'header').find_elements(By.TAG_NAME, 'a')
        links = [elem.get_attribute('href') for elem in nav_links]

        # check that 404 page navbar has link to home page
        self.assertIn(self.home, links)

    # @unittest.skip("skip")
    def test_footer_address_and_contact(self):
        """test the company address and link to email in footer"""

        driver = self.driver
        driver.get(self.home)
        footer = driver.find_element(By.TAG_NAME, 'footer')  # find footer element
        # profilence header, finding 'h2' is likely too specific and can easily fail if element changes
        profilence = footer.find_element(By.TAG_NAME, 'h2')
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

    # @unittest.skip("skip")
    def test_form(self):
        """test that form in 'contact us' has appropriate number of fields and buttons(1)"""
        driver = self.driver
        driver.get('https://www.profilence.com/contact-us/')
        # assumes that the tested form is only form in main, likely an issue
        form = driver.find_element(By.TAG_NAME, 'main').find_element(By.TAG_NAME, 'form')
        form_elements = form.find_elements(By.CLASS_NAME, 'form-element')
        self.assertEqual(8, len(form_elements))
        # check that there's exactly one button in form
        button = form.find_elements(By.TAG_NAME, 'button')
        self.assertEqual(1, len(button))

    # @unittest.skip("skip")
    def test_article_link_status_codes(self):
        """test that request to article links return status code 200"""

        driver = self.driver
        driver.get('https://www.profilence.com/news/')
        news_links = driver.find_element(By.TAG_NAME, 'main').find_elements(By.TAG_NAME, 'a')
        links = [elem.get_attribute('href') for elem in news_links]
        for item in links:
            status_code = requests.head(item).status_code  # get status code of link
            # print(f"{item}, {status_code}")
            self.assertEqual(200, status_code,
                             msg=f"{item} returned {status_code} instead of 200")

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
