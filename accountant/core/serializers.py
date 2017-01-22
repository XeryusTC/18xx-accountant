# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from rest_framework import serializers

from . import models

SOURCE_OR_DEST_REQUIRED_ERROR = \
    _('You cannot transfer money from the bank to the bank.')
DUPLICATE_SOURCE_OR_DEST_ERROR = \
    _('Cannot send or receive money to two different entities.')
DIFFERENT_GAME_ERROR = _('Sender and receiver must be part of the same game.')

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
            'game', 'cash', 'share_count', 'ipo_shares', 'bank_shares',
            'player_owners')


class PlayerShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PlayerShare
        fields = ('url', 'uuid', 'owner', 'company', 'shares')


class CompanyShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyShare
        fields = ('url', 'uuid', 'owner', 'company', 'shares')


class TransferMoneySerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    to_player = serializers.ModelField(required=False,
        model_field=models.Player._meta.get_field('uuid'))
    from_player = serializers.ModelField(required=False,
        model_field=models.Player._meta.get_field('uuid'))
    to_company = serializers.ModelField(required=False,
        model_field=models.Company._meta.get_field('uuid'))
    from_company = serializers.ModelField(required=False,
        model_field=models.Company._meta.get_field('uuid'))

    def validate(self, data):
        if 'to_player' not in data.keys() \
                and 'from_player' not in data.keys() \
                and 'to_company' not in data.keys() \
                and 'from_company' not in data.keys():
            raise serializers.ValidationError(SOURCE_OR_DEST_REQUIRED_ERROR)
        if 'from_player' in data.keys() and 'from_company' in data.keys():
            raise serializers.ValidationError(DUPLICATE_SOURCE_OR_DEST_ERROR)
        if 'to_player' in data.keys() and 'to_company' in data.keys():
            raise serializers.ValidationError(DUPLICATE_SOURCE_OR_DEST_ERROR)

        if self.source_instance != None and self.dest_instance != None:
            if self.source_instance.game != self.dest_instance.game:
                raise serializers.ValidationError(DIFFERENT_GAME_ERROR)

        return data

    @property
    def source_instance(self):
        if 'from_player' in self.initial_data.keys():
            return get_object_or_404(models.Player,
                uuid=self.initial_data['from_player'])
        if 'from_company' in self.initial_data.keys():
            return get_object_or_404(models.Company,
                uuid=self.initial_data['from_company'])
        return None

    @property
    def dest_instance(self):
        if 'to_player' in self.initial_data.keys():
            return get_object_or_404(models.Player,
                uuid=self.initial_data['to_player'])
        if 'to_company' in self.initial_data.keys():
            return get_object_or_404(models.Company,
                uuid=self.initial_data['to_company'])
        return None
