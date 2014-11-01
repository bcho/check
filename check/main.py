# coding: utf-8

'''
    check.main
    ~~~~~~~~~~

    Main function.
'''

from .watchmen import watchmen
from .meta import IncidentReport


def check(contacts, reporters, sites):
    down_sites = set()
    for watchman in watchmen.values():
        down_sites.update(watchman(sites))

    reports = list(map(IncidentReport, down_sites))

    for reporter in reporters:
        for report in reports:
            reporter(report, contacts)
