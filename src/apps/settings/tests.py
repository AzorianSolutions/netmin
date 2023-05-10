import pprint
import unittest
from django.test import Client
from django.test import TestCase


class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')

    def test_details(self):
        # Issue a GET request.
        response = self.client.get('/settings/service-packages/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        pprint.pp(response.context)

        # Check that the rendered context contains 5 customers.
        # self.assertEqual(len(response.context['records']), 5)
