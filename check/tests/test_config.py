# coding: utf-8

'''
    check.tests.test_config
    ~~~~~~~~~~~~~~~~~~~~~~~
'''

import pytest

from check.config import prepare, prepare_sites, prepare_in_charge, ConfigError


def test_prepare():
    test_configs = {
        'in_charge': [{'name': 'test-user'}],
        'reporters': {},
        'sites': [{'name': 'a-cool-site', 'url': 'http://test.domain'}]
    }
    assert len(prepare(test_configs)) == 3


def test_prepare_with_broken_configs():
    with pytest.raises(ConfigError):
        prepare({})


def test_prepare_sites():
    sites = [{'name': 'test', 'url': 'http://test.domain'}]
    for site in prepare_sites(sites):
        assert site is not None


def test_prepare_sites_with_borken_config():
    # Url is required.
    sites = [{'name': 'test'}]

    with pytest.raises(ConfigError):
        prepare_sites(sites)


def test_prepare_in_charge():
    contacts = [{'name': 'test-user-a'}, {'name': 'test-user-b'}]
    assert len(prepare_in_charge(contacts)) == len(contacts)
