# coding: utf-8

'''
    check.config
    ~~~~~~~~~~~~

    Config parser.
'''

import json

from .meta import Contact, Site
from .reporter import reporters


__all__ = ['parse_file', 'ConfigError']


class ConfigError(ValueError):
    '''Malformed configuration.'''


def prepare(raw):
    '''Clean a config.

    :param raw: raw config.
    '''
    try:
        return (
            prepare_in_charge(raw['in_charge']),
            prepare_reporters(raw['reporters']),
            prepare_sites(raw['sites'])
        )
    except KeyError:
        # TODO handle error gracefully.
        raise ConfigError


def prepare_in_charge(raw):
    '''Parse men in charge's information.

    :param raw: raw config.
    '''
    if not isinstance(raw, list):
        raw = [raw]

    return [Contact.from_dict(config) for config in raw]


def prepare_reporters(raw):
    '''Parse reporters settings.

    :param raw: raw config.
    '''
    required = []
    for name, configs in raw.items():
        try:
            MakeReporter = reporters[name]
        except KeyError:
            raise ConfigError('Unable to find reporter {0}'.format(name))
        try:
            formats = configs.pop('formats')
        except KeyError:
            raise ConfigError(
                'Should specify report format for {0}.'.format(name)
            )
        required.append(MakeReporter(formats=formats, **configs))

    return required


def prepare_sites(raw):
    '''Parse sites settings.

    :param raw: raw config.
    '''
    sites = []
    for site in raw:
        if 'url' not in site:
            raise ConfigError('url is required.')
        sites.append(Site.from_dict(site))
    return sites


def parse_file(filename):
    with open(filename, 'r') as f:
        return prepare(json.load(f))
