from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # open a website
        self.browser.get('http:\\localhost:8000')

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
        table = self.browser.find_element_by_id('id_list_table')
        rows = self.browser.find_elements_by_tag_name('tr')
        self.assertTrue(any(row.text == '1: Buy peacock feathers' for row in rows), "no such element in table")

        self.fail('end of test')


if __name__ == '__main__':
    unittest.main()


# on website there should be an empty text field for a new thing to do

# type in a new field: use peacock feather to make a bait

# website content should be updated and displayed: now 2 things to do should occur

# check if website saves the list, url address should be generated with text box with description

# if url address is opened in website, saved list with things to do should appear

# close the website
