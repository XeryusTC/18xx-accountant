# -*- coding: utf-8 -*-
from rest_framework import serializers

from . import models

class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Game
        fields = ('url', 'uuid',)
