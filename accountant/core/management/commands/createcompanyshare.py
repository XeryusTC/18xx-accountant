# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

from core.models import Company, CompanyShare

class Command(BaseCommand):
    help = 'Gives a company shares in a company'

    def add_arguments(self, parser):
        parser.add_argument('owner')
        parser.add_argument('company')
        parser.add_argument('--shares', type=int, default=1)

    def handle(self, *args, **options):
        try:
            owner = Company.objects.get(pk=options['owner'])
            company = Company.objects.get(pk=options['company'])
        except Company.DoesNotExist:
            raise CommandError('This is not a valid UUID')
        if owner.game != company.game:
            raise CommandError('Owner and company are not in the same game')

        share, created = CompanyShare.objects.get_or_create(owner=owner,
            company=company)
        share.shares = options['shares']
        share.save()

        self.stdout.write(str(share.pk))
