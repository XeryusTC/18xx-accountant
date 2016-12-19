# -*- coding: utf-8 -*-
from django.db import models
import uuid

colors = ('red', 'pink', 'purple', 'deep purple', 'indigo', 'blue',
    'light blue', 'cyan', 'teal', 'green', 'light green', 'lime', 'yellow',
    'amber', 'orange', 'deep orange', 'brown', 'grey', 'blue grey')
shades = (50,) + tuple(range(100, 1000, 100))
color_options = ('black', 'white') + \
    tuple(('{} {}'.format(c, s) for c in colors for s in shades))

class Game(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
        editable=False)


class Player(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=16, default='Player')
    game = models.ForeignKey(Game, related_name='players')

class Company(models.Model):
    COLOR_CODES = tuple(((opt.replace(' ', '-'), opt.title())
        for opt in color_options))

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=8, default='Company')
    game = models.ForeignKey(Game, related_name='companies')
    text_color = models.CharField(max_length=16, choices=COLOR_CODES,
        default='black', blank=False)
    background_color = models.CharField(max_length=16, choices=COLOR_CODES,
        default='white', blank=False)
