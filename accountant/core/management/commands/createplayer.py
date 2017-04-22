# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from core.models import Game, Player

class Command(BaseCommand):
    help = 'Creates a player'

    def add_arguments(self, parser):
        parser.add_argument('game')
        parser.add_argument('name')
        parser.add_argument('--cash', type=int, default=0)

    def handle(self, *args, **options):
        try:
            game = Game.objects.get(pk=options['game'])
        except ValueError as ex:
            raise CommandError('This is not a valid UUID')
        player = Player.objects.create(game=game, name=options['name'],
            cash=options['cash'])
        self.stdout.write(str(player.pk))
