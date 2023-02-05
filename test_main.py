import pytest
import webscrap


@pytest.fixture(name="analizy_web")
def fixture_analizy_web():
    analizy_web = webscrap.GetAssetAnalizy("analizy.pl")
    yield analizy_web
