# coding: utf-8

'''
    check.reporter
    ~~~~~~~~~~~~~~

    Reporters collection.
'''

import smtplib
from sys import stderr
from email.mime.text import MIMEText
from contextlib import contextmanager


__all__ = ['BaseReporter', 'FileObjectReporter', 'EmailReporter', 'reporters']


class BaseReporter(object):
    '''Base report generator.

    :param formats: output formats map,
                    contains ``short`` and ``long``.
    '''

    def __init__(self, formats):
        self.formats = formats

    def render(self, report):
        '''Render report.

        :param report: a :class:`check.meta.IncidentReport` instance.
        '''
        return {s: f.format(**report) for s, f in self.formats.items()}

    def generate(self, incident_report, contacts, *args, **kwargs):
        '''Generate and deliver a incident report.

        :param incident_report: a :class:`check.meta.IncidentReport` instance.
        :param contacts: list of :class:`meta.Contact`.
        '''
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        return self.generate(*args, **kwargs)


class FileObjectReporter(BaseReporter):
    '''Print report to a file object.

    :param output: output file object, defaults to `sys.stderr`.
    '''

    # Output tempalte.
    output_tmpl = '{short}\n{long}\n'

    def __init__(self, formats, output=None):
        super(FileObjectReporter, self).__init__(formats)

        if output is None:
            output = stderr
        self._output = output

    def generate(self, incident_report, *args, **kwargs):
        report = self.render(incident_report)

        self._output.write(self.output_tmpl.format(**report))


class EmailReporter(BaseReporter):
    '''Email reporter.

    :param username: sender login name.
    :param password: sender password.
    :param smtp: mail server.
    '''

    def __init__(self, formats, username, password, smtp):
        super(EmailReporter, self).__init__(formats)
        self._crends = {
            'username': username,
            'password': password,
            'smtp': smtp
        }

    def generate(self, incident_report, contacts, *args, **kwargs):
        receivers = [c.email for c in contacts if c.email is not None]
        if not receivers:
            return

        mail = self._build_mail(incident_report).as_string()
        with self._start_smtp_server() as server:
            server.sendmail(self._crends['username'], receivers, mail)

    @contextmanager
    def _start_smtp_server(self):
        '''Start a smtp connection.'''
        server = smtplib.SMTP(self._crends['smtp'])
        server.starttls()
        server.login(self._crends['username'], self._crends['password'])
        yield server
        server.quit()

    def _build_mail(self, incident_report):
        '''Build a mail from report.

        :param incident_report: a :class:`check.meta.IncidentReport` instance.
        '''
        subject = self.formats['short'].format(**incident_report)
        content = self.formats['long'].format(**incident_report)

        mail = MIMEText(content, 'plain')
        mail['Subject'] = subject
        mail['From'] = self._crends['username']

        return mail


def make_email_reporter_from_config(formats, crendential, *args, **kwargs):
    kwargs.update(crendential)
    return EmailReporter(formats=formats, *args, **kwargs)


# Exposed reporters.
reporters = {
    'cli': FileObjectReporter,
    'email': make_email_reporter_from_config
}
