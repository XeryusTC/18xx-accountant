# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from core.models import Game, Company

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('game')
        parser.add_argument('name')
        parser.add_argument('--cash', type=int, default=0)
        parser.add_argument('--shares', dest='share_count', type=int,
            default=10)
        parser.add_argument('--ipo', dest='ipo_shares', type=int, default=10)
        parser.add_argument('--bank', dest='bank_shares', type=int, default=0)

    def handle(self, *args, **options):
        try:
            game = Game.objects.get(pk=options['game'])
        except ValueError:
            raise CommandError('This is not a valid UUID')
        company = Company.objects.create(game=game, name=options['name'],
            cash=options['cash'], share_count=options['share_count'],
            ipo_shares=options['ipo_shares'],
            bank_shares=options['bank_shares'])
        return str(company.pk)