"""Loader and executor of finscrap module."""

import json
import click

from finscrap import finscrap


@click.command()
@click.argument("filename")
def read_config(filename):
    "Load funds config as dictionary"
    with open(filename, "r", encoding="utf-8") as fund_config:
        funds_urls = json.load(fund_config)

    analizy = finscrap.GetAssetAnalizy("analizy.pl", funds_urls)
    analizy.get_data()

    biznesr = finscrap.GetAssetBiznesR("biznesradar.pl", funds_urls)
    biznesr.get_data()

    borsa = finscrap.GetAssetBorsa("borsa", funds_urls)
    borsa.get_data()

    ishares = finscrap.GetAssetIShares("ishares", funds_urls)
    ishares.get_data()


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    read_config()
