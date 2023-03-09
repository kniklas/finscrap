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

    webscapper = finscrap.GetData(funds_urls)

    if csv:
        webscapper.out_csv(csv)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    read_config()
