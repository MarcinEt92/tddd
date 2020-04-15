from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time


# before we inherited from unittest.TestCase
class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = self.browser.find_elements_by_tag_name('tr')

        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # open a website
        # self.browser.get('http:\\localhost:8000')
        self.browser.get(self.live_server_url)

        # website and header should contain name 'Lists'
        self.assertIn('List', self.browser.title, 'browser title is actually: ' + self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('List', header_text)

        # encouraged to type one thing to do
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Type a thing to do...')

        # type in text field: Buy peacock feathers
        input_box.send_keys('Buy peacock feathers')

        # type Enter and then site content is updated and displayed
        input_box.send_keys(Keys.ENTER)

        # this part of test was added later (page 104), there should be specific url for new list creation
        # after writing and confirming 1st thing to do we should be redirected to url below
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        # end of part (page 104)

        #  time.sleep(10)

        self.check_for_row_in_list_table("1: Buy peacock feathers")

        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use peacock feather to make a bait')
        input_box.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feather to make a bait')

        # next park of testing (page 104) a new user Frank starts using our website
        # we start a new web session, no information from previous user's list should be displayed now
        self.browser.quit()
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('feather to make a bait', page_text)

        # Frank types his thing to do
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy milk')
        input_box.send_keys(Keys.ENTER)

        # after that we expect unique url address for user's own list
        frank_list_url = self.browser.current_url
        # we check if the address is what we planned (a new address for new list creation)
        self.assertRegex(frank_list_url, '/lists/.+')
        # Edith anf Frank list urls should not be the same
        self.assertNotEqual(edith_list_url, frank_list_url)

        # we check again that in Frank list there is no element from Edith list
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        self.fail('end of test')


# if Django test engine is being used this code is nor necessary
# if __name__ == '__main__':
#     unittest.main()


# on website there should be an empty text field for a new thing to do

# type in a new field: use peacock feather to make a bait

# website content should be updated and displayed: now 2 things to do should occur

# check if website saves the list, url address should be generated with text box with description

# if url address is opened in website, saved list with things to do should appear

# close the website
