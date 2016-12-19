# -*- coding: utf-8 -*-
from rest_framework import serializers

from . import models

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Game
        fields = ('url', 'uuid', 'players', 'companies')


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Player
        fields = ('url', 'uuid', 'name', 'game', 'cash', 'shares')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = ('url', 'uuid', 'name', 'text_color', 'background_color',
            'game', 'cash', 'shares', 'ipo_shares', 'bank_shares', 'owners')


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Share
        fields = ('url', 'uuid', 'player', 'company', 'shares')
