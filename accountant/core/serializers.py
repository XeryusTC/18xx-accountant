# -*- coding: utf-8 -*-
from rest_framework import serializers

from . import models

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Game
        fields = ('uuid', 'players', 'companies')


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Player
        fields = ('uuid', 'name', 'game')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = ('uuid', 'name', 'text_color', 'background_color',
            'game')
