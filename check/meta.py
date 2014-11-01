# coding: utf-8

'''
    check.meta
    ~~~~~~~~~~
'''

import arrow


class Contact(object):
    '''Contact information.

    :param name: contact's name.
    :param email: contact's email (optional).
    '''

    def __init__(self, name, email=None):
        self.name = name
        self.email = email

    def __str__(self):
        return '<Contact: {r.name}>'.format(r=self)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_dict(cls, d):
        '''Create from dict structure.'''
        return Contact(**d)


class Site(dict):
    '''Site information.

    :param url: site's url.
    :param name: site alias name (optional).
    '''

    def __init__(self, url, name=None):
        self['url'] = url
        self['name'] = name or url

    def __str__(self):
        return '<Site: {r.name}:{r.url}>'.format(r=self)

    def __repr__(self):
        return self.__str__()

    def __getattr__(self, key):
        return self[key]

    def __hash__(self):
        return hash(self['url'])

    @classmethod
    def from_dict(cls, d):
        '''Create from dict structure.'''
        return Site(**d)


class IncidentReport(dict):
    '''Incident report.

    TODO review this structure

    :param site: a :class:`Site` instance.
    '''

    def __init__(self, site):
        self['site'] = site
        self['happened_at'] = arrow.utcnow()

    def __getattr__(self, key):
        return self[key]
