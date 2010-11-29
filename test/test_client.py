import time
import random
import unittest
from jsonutil import jsonutil as json
import random
from simplegeo.places import Client, Record, APIError

from decimal import Decimal as D

import os

import mock

MY_OAUTH_KEY = 'MY_OAUTH_KEY'
MY_OAUTH_SECRET = 'MY_SECRET_KEY'
TESTING_LAYER = 'TESTING_LAYER'

API_VERSION = '1.0'
API_HOST = 'api.simplegeo.com'
API_PORT = 80

# example: http://api.simplegeo.com/0.1/context/37.797476,-122.424082.json

class ClientTest(unittest.TestCase):
    def setUp(self):
        self.client = Client(MY_OAUTH_KEY, MY_OAUTH_SECRET, API_VERSION, API_HOST, API_PORT)
        self.query_lat = D('37.8016')
        self.query_lon = D('-122.4783')

    def _record(self):
        self.record_id += 1
        self.record_lat = (self.record_lat + 10) % 90
        self.record_lon = (self.record_lon + 10) % 180

        return Record(
            layer=TESTING_LAYER,
            id=str(self.record_id),
            lat=self.record_lat,
            lon=self.record_lon
        )

    def test_wrong_endpoint(self):
        self.assertRaises(Exception, self.client.endpoint, 'wrongwrong')

    def test_missing_argument(self):
        self.assertRaises(Exception, self.client.endpoint, 'context')

    def test_get_context(self):
        xyz make a bunch of things

        mockhttp = mock.Mock()
        mockhttp.request.return_value = ({'status': '200', 'content-type': 'application/json', }, resultrecord.to_json())
        self.client.http = mockhttp

        res = self.client.get_context(self.query_lat, self.query_lon)
        self.assertEqual(mockhttp.method_calls[0][0], 'request')
        self.assertEqual(mockhttp.method_calls[0][1][0], 'http://api.simplegeo.com:80/%s/places/%s.json' % (API_VERSION, simplegeoid))
        self.assertEqual(mockhttp.method_calls[0][1][1], 'GET')
        self.failUnless(isinstance(res, Record), res)
        self.assertEqual(res.to_json(), resultrecord.to_json())
