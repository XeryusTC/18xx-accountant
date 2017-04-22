# -*- coding: utf-8 -*-
from django.test.runner import DiscoverRunner

class StagingTestRunner(DiscoverRunner): # pragma: no cover
    @classmethod
    def add_arguments(cls, parser):
        super(StagingTestRunner, cls).add_arguments(parser)
        parser.add_argument('-s', '--staging', default=False, nargs=2,
            metavar=('URL', 'INVENTORY'),
            help='Run the functional tests against a remote server instead of '
                'locally. URL is the address where the website can be '
                'reached. INVENTORY is the location of the Ansible iventory '
                'file describing how to reach the server.')
        parser.add_argument('-a', '--ansible-directory', metavar='DIR',
            default='../deploy/',
            help='Location of where Ansible playbooks can be found')
