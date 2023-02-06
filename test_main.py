import pytest
import requests
import bs4
from urllib import request
from unittest.mock import patch

import webscrap

ANALIZY_PL = """
<p class=\'lightProductText\'>12.2</p>
<span class=\'productBigText\'>2022-12-01</span>
"""

# TODO
# - HTTPError and URLError
# - get_element() catch errors with incorrect tag or class_id - AttributeError
# - confirm scenarios where date or price == None


class DummySoup(bs4.BeautifulSoup):
    def __init__(self):
        super().__init__(ANALIZY_PL, "lxml")


class DummyRequestGet():
    def __init__(self):
        self.content = "Request Get Dummy content"


class DummyRequest():
    def __init__(self):
        self.full_url = "http://dummy-url.com/somepage.html"
        self.host = "dummy-url.com"


@pytest.fixture(name="analizy_web")
def fixture_analizy_web():
    analizy_web = webscrap.GetAssetAnalizy("analizy.pl")
    yield analizy_web


@pytest.fixture(name="biznesradar_web")
def fixture_biznesradar_web():
    biznesradar_web = webscrap.GetAssetAnalizy("biznesradar.pl")
    yield biznesradar_web


def test_analizy_pl_initialisation(analizy_web):
    assert analizy_web


def test_biznesradar_pl_initialisation(biznesradar_web):
    assert biznesradar_web


@patch.object(request, "Request", return_value=DummyRequest())
@patch.object(request, "urlopen", return_value="urlopen Web Response")
@patch.object(requests, "get", return_value=DummyRequestGet())
@patch.object(bs4, "BeautifulSoup", return_value=DummySoup())
def test_analizy_get_data(mock_Request, mock_urlopen, mock_get,
                          mock_BeautifulSoup, analizy_web):
    result = analizy_web.get_data()
    assert result == {'I01': ('12.2', '2022-12-01')}
