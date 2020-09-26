from pytest import unittest
from nordapi.NordApi import NordApi


class TestCountryExists(unittest.TestCase):
    def test_valid_country(self):
        valid = NordApi()
        assert type(valid.get_country_id('australia')) == int

    def test_invalid_country(self):
        invalid = NordApi()
        self.assertRaises(Exception, invalid.get_country_id('erie'))


class TestGetRecommended(unittest.TestCase):
    def test_valid_getrecom(self):
        valid = NordApi()
        valid.get_country_id('croatia')
        assert type(valid.get_recommended().json()) == dict
