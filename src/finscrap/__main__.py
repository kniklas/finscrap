"""Loader and executor of finscrap module."""

import json
import click

from finscrap import finscrap


@click.command()
@click.argument("funds_json", type=click.Path(exists=True))
@click.option("-c", "--csv", type=click.Path(), help="Path to CSV output file")
def read_config(funds_json, csv):
    """Reads funds prices and valuation dates from defined URLs via FUNDS_JSON
    definition file.
    """
    with open(funds_json, "r", encoding="utf-8") as fund_config:
        funds_urls = json.load(fund_config)

    print("OUTPUT_CSV", csv)
    analizy = finscrap.GetAssetAnalizy("analizy.pl", funds_urls)
    analizy.get_data()

    #  biznesr = finscrap.GetAssetBiznesR("biznesradar.pl", funds_urls)
    #  biznesr.get_data()

    #  borsa = finscrap.GetAssetBorsa("borsa", funds_urls)
    #  borsa.get_data()

    #  ishares = finscrap.GetAssetIShares("ishares", funds_urls)
    #  ishares.get_data()


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    read_config()
