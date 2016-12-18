# -*- coding: utf-8 -*-
from django.db import models
import uuid

class Game(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
        editable=False)


class Player(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=16, default='Player')
    game = models.ForeignKey(Game, related_name='players')
