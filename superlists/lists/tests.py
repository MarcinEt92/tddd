from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
import re

csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_root_url_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        observed_html = re.sub(csrf_regex, '', response.content.decode())
        expected_html = render_to_string('home.html')
        self.assertEqual(observed_html, expected_html)

        # do not test constants like below:
        # self.assertTrue(response.content.startswith(b'<!DOCTYPE html>'))
        # self.assertIn(b'<title>List of things to do</title>', response.content)
        # self.assertTrue(response.content.endswith(b'</html>'))

    def test_home_page_can_save_a_post_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'New list item'

        response = home_page(request)

        self.assertIn('New list item', response.content.decode())

        observed_html = re.sub(csrf_regex, '', response.content.decode())

        #  we are passing new_item_text to a template
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'New list item'}
        )

        self.assertEqual(observed_html, expected_html)

        #  response.content.decode() - html code generated by views function
        #  render_to_string() - manually generated template

