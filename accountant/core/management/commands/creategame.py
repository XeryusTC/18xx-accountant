# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from core.models import Game

class Command(BaseCommand):
    help = 'Creates a new game'

    def add_arguments(self, parser):
        parser.add_argument('--cash', type=int, default=12000)

    def handle(self, *args, **options):
        game = Game.objects.create(cash=options['cash'])
        self.stdout.write(str(game.pk))
