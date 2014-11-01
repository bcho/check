# coding: utf-8

'''
    check.watchmen
    ~~~~~~~~~~~~~~

    Server status watchmen.
'''

import requests


__all__ = ['BaseWatchmen', 'HTTPWatchmen', 'watchmen']


class BaseWatchmen(object):
    '''Base watchmen.'''

    def check(self, sites):
        '''Check a list of sites and return sites that is down.

        :param sites: list of :class:`check.meta.Site` instances
        '''
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        return self.check(*args, **kwargs)


class HTTPWatchmen(BaseWatchmen):
    '''Watch over HTTP.'''

    def check(self, sites):
        return list(filter(None, map(self.get_site, sites)))

    def get_site(self, site):
        '''Touch a site with a GET call.
        Returns incident report if the response is not 2xx.
        '''
        try:
            resp = requests.get(site.url)
        except Exception:
            return site

        if not resp.ok:
            return site


# Exposed watchmen.
watchmen = {
    'http': HTTPWatchmen()
}
