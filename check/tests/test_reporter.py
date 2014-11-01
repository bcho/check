# coding: utf-8

'''
    check.tests.test_reporter
    ~~~~~~~~~~~~~~~~~~~~~~~~~
'''

import pytest
from io import StringIO

from check.meta import Site, IncidentReport
from check.reporter import FileObjectReporter


@pytest.fixture
def incident_report():
    return IncidentReport(Site(url='http://test.domain', name='test'))


@pytest.fixture
def report_format():
    return {
        'short': '{site.name}',
        'long': '{site.url}'
    }


@pytest.fixture
def file_object_reporter_and_buffer(report_format):
    output_buf = StringIO()
    reporter = FileObjectReporter(report_format, output_buf)

    return reporter, output_buf


def test_file_object_reporter(incident_report,
                              file_object_reporter_and_buffer):
    reporter, buf = file_object_reporter_and_buffer
    reporter(incident_report)

    output = buf.getvalue().strip()
    assert output is not None
    assert len(output.split('\n')) == 2
