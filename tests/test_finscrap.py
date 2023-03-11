# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import urllib
import json
from urllib import request
from urllib.error import HTTPError
from urllib.error import URLError

import pytest
import requests
import bs4

# pylint: disable=import-error
from finscrap import finscrap


ANALIZY_PL = """
<span class=\'productBigText\'>12.2</span>
<p class=\'lightProductText\'>01.12.2022</p>
"""

ANALIZY_PL_BAD_PRICE_CLASS = """
<span class=\'productBigText2\'>12.2</span>
<p class=\'lightProductText\'>01.12.2022</p>
"""

ANALIZY_PL_BAD_DATE_CLASS = """
<span class=\'productBigText\'>12.2</span>
<p class=\'lightProductText2\'>01.12.2022</p>
"""

ANALIZY_PL_BAD_PRICE_TAG = """
<l class=\'productBigText\'>12.2</l>
<p class=\'lightProductText\'>01.12.2022</p>
"""

ANALIZY_PL_BAD_DATE_TAG = """
<span class=\'productBigText\'>12.2</span>
<l class=\'lightProductText\'>01.12.2022</l>
"""

TEST_DATA = "tests/funds.json"


# pylint: disable=too-few-public-methods
# pylint: disable=abstract-method
class DummySoup(bs4.BeautifulSoup):
    def __init__(self, in_soup):
        super().__init__(in_soup, "lxml")


class DummyRequestGet:
    def __init__(self):
        self.content = "Request Get Dummy content"


@pytest.fixture(name="test_data")
def fixture_test_data():
    with open(TEST_DATA, "r", encoding="utf-8") as fund_config:
        test_data = json.load(fund_config)
    yield test_data


@pytest.fixture(name="analizy_web")
def fixture_analizy_web(test_data):
    analizy_web = finscrap.GetAssetAnalizy("analizy.pl", test_data)
    yield analizy_web


@pytest.fixture(name="borsa_web")
def fixture_borsa_web(test_data):
    borsa_web = finscrap.GetAssetBorsa("borsa", test_data)
    yield borsa_web


@pytest.fixture(name="ishares_web")
def fixture_ishares_web(test_data):
    ishares_web = finscrap.GetAssetIShares("ishares", test_data)
    yield ishares_web


@pytest.fixture(name="data_wrapper")
def fixture_data_wrapper():
    data_wrapper = finscrap.GetData(TEST_DATA)
    yield data_wrapper


def test_dict_to_list_conversion(data_wrapper):
    test_dict = {
        "I01": ("2023-03-09", "97.27"),
        "PLALIOR00169": ("2023-03-10", "101.73"),
    }
    result = [
        ["I01", "2023-03-09", "97.27"],
        ["PLALIOR00169", "2023-03-10", "101.73"],
    ]
    assert data_wrapper.dict_to_list(test_dict) == result


def test_data_wrapper_get_data(mocker, data_wrapper):
    """Testing if GetData.get_data() method returns dictionary consiting set of
    all providers dictionaries."""
    mocker.patch.object(
        data_wrapper.analizy_obj, "get_data", return_value={"01": "ALA"}
    )
    mocker.patch.object(
        data_wrapper.biznesr_obj, "get_data", return_value={"02": "CAT"}
    )
    mocker.patch.object(
        data_wrapper.borsa_obj, "get_data", return_value={"03": "OLD"}
    )
    mocker.patch.object(
        data_wrapper.ishares_obj, "get_data", return_value={"04": "KYC"}
    )
    data_wrapper.get_data()
    assert data_wrapper.data_dict == {
        "01": "ALA",
        "02": "CAT",
        "03": "OLD",
        "04": "KYC",
    }


def test_data_wrapper_csv_saving(mocker, data_wrapper):
    mocked_data = mocker.mock_open(read_data="")
    mocked_file = mocker.patch("builtins.open", mocked_data)
    data_wrapper.out_csv("file.csv")
    mocked_file.assert_called_with(
        "file.csv", "w", newline="", encoding="utf-8"
    )


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


def test_biznesradar_pl_initialisation(test_data):
    biznesradar_web = finscrap.GetAssetAnalizy("biznesradar.pl", test_data)
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
        (ANALIZY_PL_BAD_PRICE_CLASS, "span", "productBigText"),
        (ANALIZY_PL_BAD_PRICE_TAG, "span", "productBigText"),
        (ANALIZY_PL_BAD_DATE_CLASS, "p", "lightProductText"),
        (ANALIZY_PL_BAD_DATE_TAG, "p", "lightProductText"),
    ),
)
def test_analizy_get_element_exception(analizy_web, html, tag, id_):
    with pytest.raises(AttributeError):
        soup = bs4.BeautifulSoup(html, "lxml")
        analizy_web.get_element(soup, tag, id_)


@pytest.mark.parametrize(
    "html, expected_result",
    (
        (ANALIZY_PL, {"I01": ("2022-12-01", "12.2")}),
        (ANALIZY_PL_BAD_PRICE_CLASS, {"I01": ("2022-12-01", None)}),
        (ANALIZY_PL_BAD_DATE_CLASS, {"I01": (None, "12.2")}),
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
        (
            "p",
            "lightProductText",
            '<p class="lightProductText">01.12.2022</p>',
        ),
        (
            "span",
            "productBigText",
            '<span class="productBigText">12.2</span>',
        ),
    ),
)
def test_analizy_get_element_found(analizy_web, tag, id_, expected_result):
    soup = bs4.BeautifulSoup(ANALIZY_PL, "lxml")
    assert str(analizy_web.get_element(soup, tag, id_)) == expected_result
