# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import urllib
from urllib import request
from urllib.error import HTTPError
from urllib.error import URLError

import pytest
import requests
import bs4

# pylint: disable=import-error
from finscrap import finscrap


ANALIZY_PL = """
<p class=\'lightProductText\'>12.2</p>
<span class=\'productBigText\'>2022-12-01</span>
"""

ANALIZY_PL_BAD_PRICE_CLASS = """
<p class=\'lightProductText2\'>12.2</p>
<span class=\'productBigText\'>2022-12-01</span>
"""

ANALIZY_PL_BAD_DATE_CLASS = """
<p class=\'lightProductText\'>12.2</p>
<span class=\'productBigText2\'>2022-12-01</span>
"""

ANALIZY_PL_BAD_PRICE_TAG = """
<l class=\'lightProductText\'>12.2</l>
<span class=\'productBigText2\'>2022-12-01</span>
"""

ANALIZY_PL_BAD_DATE_TAG = """
<p class=\'lightProductText\'>12.2</p>
<div class=\'productBigText2\'>2022-12-01</div>
"""


# pylint: disable=too-few-public-methods
# pylint: disable=abstract-method
class DummySoup(bs4.BeautifulSoup):
    def __init__(self, in_soup):
        super().__init__(in_soup, "lxml")


class DummyRequestGet:
    def __init__(self):
        self.content = "Request Get Dummy content"


@pytest.fixture(name="analizy_web")
def fixture_analizy_web():
    analizy_web = finscrap.GetAssetAnalizy("analizy.pl")
    yield analizy_web


@pytest.fixture(name="borsa_web")
def fixture_borsa_web():
    borsa_web = finscrap.GetAssetBorsa("borsa")
    yield borsa_web


@pytest.fixture(name="ishares_web")
def fixture_ishares_web():
    ishares_web = finscrap.GetAssetIShares("ishares")
    yield ishares_web


def test_borsa_date_conversion(borsa_web):
    input_date = "23/02/10"
    assert borsa_web.convert_date(input_date) == "2023-02-10"


def test_analizy_date_conversion(analizy_web):
    input_date = "09.02.2023"
    assert analizy_web.convert_date(input_date) == "2023-02-09"


def test_ishares_date_conversion(ishares_web):
    input_date = "Feb/09/2023"
    assert ishares_web.convert_date(input_date) == "2023-02-09"


def test_analizy_pl_initialisation(analizy_web):
    assert analizy_web


def test_ishares_initialisation(ishares_web):
    assert ishares_web


def test_biznesradar_pl_initialisation():
    biznesradar_web = finscrap.GetAssetAnalizy("biznesradar.pl")
    assert biznesradar_web


def test_concatenate_date(analizy_web):
    assert analizy_web.concatenate_date("01", "02", "2022") == "2022-02-01"


def test_get_data_raise_url_error(mocker, analizy_web):
    mocker.patch.object(
        urllib.request,
        "urlopen",
        side_effect=URLError("BAD URL"),
    )
    result = analizy_web.get_data()
    assert result == {"I01": (None, None)}


def test_get_data_raise_http_error(mocker, analizy_web):
    mocker.patch.object(
        urllib.request,
        "urlopen",
        side_effect=HTTPError("OJ!", 404, "aa", None, None),
    )
    result = analizy_web.get_data()
    assert result == {"I01": (None, None)}


@pytest.mark.parametrize(
    "html, tag, id_",
    (
        (ANALIZY_PL_BAD_PRICE_CLASS, "p", "lightProductText"),
        (ANALIZY_PL_BAD_PRICE_TAG, "p", "lightProductText"),
        (ANALIZY_PL_BAD_DATE_CLASS, "span", "productBigText"),
        (ANALIZY_PL_BAD_DATE_TAG, "span", "productBigText"),
    ),
)
def test_analizy_get_element_exception(analizy_web, html, tag, id_):
    with pytest.raises(AttributeError):
        soup = bs4.BeautifulSoup(html, "lxml")
        analizy_web.get_element(soup, tag, id_)


@pytest.mark.parametrize(
    "html, expected_result",
    (
        (ANALIZY_PL, {"I01": ("12.2", "2022-12-01")}),
        (ANALIZY_PL_BAD_PRICE_CLASS, {"I01": (None, "2022-12-01")}),
        (ANALIZY_PL_BAD_DATE_CLASS, {"I01": ("12.2", None)}),
    ),
)
def test_analizy_get_data(mocker, analizy_web, html, expected_result):
    mocker.patch.object(request, "urlopen", return_value="urlopen web res")
    mocker.patch.object(requests, "get", return_value=DummyRequestGet())
    mocker.patch.object(bs4, "BeautifulSoup", return_value=DummySoup(html))
    result = analizy_web.get_data()
    assert result == expected_result


# pylint: disable=fixme
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
def test_analizy_get_element_found(analizy_web, tag, id_, expected_result):
    soup = bs4.BeautifulSoup(ANALIZY_PL, "lxml")
    assert str(analizy_web.get_element(soup, tag, id_)) == expected_result
