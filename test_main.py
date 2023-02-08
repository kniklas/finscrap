import pytest
import requests
import bs4
import urllib
from urllib import request
from urllib.error import HTTPError
from urllib.error import URLError

#  from unittest.mock import patch

import webscrap

ANALIZY_PL = """
<p class=\'lightProductText\'>12.2</p>
<span class=\'productBigText\'>2022-12-01</span>
"""

ANALIZY_PL_bad_price_class = """
<p class=\'lightProductText2\'>12.2</p>
<span class=\'productBigText\'>2022-12-01</span>
"""

ANALIZY_PL_bad_date_class = """
<p class=\'lightProductText\'>12.2</p>
<span class=\'productBigText2\'>2022-12-01</span>
"""

# TODO
# - test HTTPError and URLError (mock exception in request.urlopen() and verify
# if date and price have value of None, None
# - extract correct tags/class configuration to variables in test / parametrize
# test data
# - add test coverage


class DummySoup(bs4.BeautifulSoup):
    def __init__(self, in_soup):
        super().__init__(in_soup, "lxml")


class DummyRequestGet:
    def __init__(self):
        self.content = "Request Get Dummy content"


class DummyRequest:
    def __init__(self):
        self.full_url = "http://dummy-url.com/somepage.html"
        self.host = "dummy-url.com"


# TODO: CONSIDER REMOVING / REFACTORING (duplicate?)
class DummyURLLibRequestHTTPError:
    def __init__(self):
        super().__init__()
        print("initiate HTTP Error class object")

    @staticmethod
    def urlopen():
        print("request.urlopen - raise HTTPError")
        raise HTTPError("URL", 404, "Not found", None, None)


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


#  @pytest.mark.skip
@pytest.mark.parametrize(
    "html, expected_result",
    (
        (ANALIZY_PL, {"I01": ("12.2", "2022-12-01")}),
        (ANALIZY_PL_bad_price_class, {"I01": (None, "2022-12-01")}),
        (ANALIZY_PL_bad_date_class, {"I01": ("12.2", None)}),
    ),
)
def test_get_data(mocker, analizy_web, html, expected_result):
    mocker.patch.object(request, "urlopen", return_value="urlopen web res")
    mocker.patch.object(request, "Request", return_value=DummyRequest())
    mocker.patch.object(requests, "get", return_value=DummyRequestGet())
    # TODO: can above 3 line be part of fixture? / CHECK /
    mocker.patch.object(bs4, "BeautifulSoup", return_value=DummySoup(html))
    result = analizy_web.get_data()
    assert result == expected_result


class ERO:
    @staticmethod
    def urlopen():
        print("Raise URL/HTTPError")
        #  raise ValueError
        #  raise HTTPError("URL", 404, "Not found", None, None)
        raise URLError("missing url")


# TODO
# - check if above static method can be simple method
# - add HTTPError handling/testing.
def test_get_data_raise_exception(mocker, analizy_web):
    mocker.patch.object(
        urllib.request,
        "urlopen",
        side_effect=URLError("BAD URL"),
    )
    mocker.patch.object(request, "Request", return_value=DummyRequest())
    mocker.patch.object(requests, "get", return_value=DummyRequestGet())
    mocker.patch.object(bs4, "BeautifulSoup", return_value=DummySoup(""))
    result = analizy_web.get_data()
    #  print(result)
    assert result == {"I01": (None, None)}


@pytest.mark.parametrize(
    "html, tag, id_",
    (
        (ANALIZY_PL_bad_price_class, "p", "lightProductText"),
        (ANALIZY_PL_bad_date_class, "span", "productBigText"),
    ),
)
def test_get_element_exception(analizy_web, html, tag, id_):
    with pytest.raises(AttributeError):
        soup = bs4.BeautifulSoup(html, "lxml")
        analizy_web.get_element(soup, tag, id_)


# TODO: consider if this is not duplicate of test_get_data()
@pytest.mark.parametrize(
    "tag, id_, expected_result",
    (
        ("p", "lightProductText", '<p class="lightProductText">12.2</p>'),
        (
            "span",
            "productBigText",
            '<span class="productBigText">2022-12-01</span>',
        ),
    ),
)
def test_get_element_found(analizy_web, tag, id_, expected_result):
    soup = bs4.BeautifulSoup(ANALIZY_PL, "lxml")
    assert str(analizy_web.get_element(soup, tag, id_)) == expected_result
