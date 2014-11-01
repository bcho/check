# coding: utf-8

'''
    check.cli
    ~~~~~~~~~

    Commandline entry point.
'''

import click

from .config import parse_file
from .main import check


@click.command()
@click.option('--config', '-c', help='Config.json', required=True,
              type=click.Path(exists=True))
def main(config):
    parsed_config = parse_file(config)
    check(*parsed_config)
