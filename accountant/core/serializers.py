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
BUYER_REQUIRED_ERROR = _('You need to specify who buys the share')
SOURCE_REQUIRED_ERROR = _('You need to specify where the share comes from')
DUPLICATE_COMPANY_ERROR = \
    _('There is already a company with this name in your game')
DUPLICATE_PLAYER_ERROR = \
    _('There is already a player with this name in your game')

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Game
        fields = ('url', 'uuid', 'players', 'companies', 'cash',
            'pool_shares_pay', 'ipo_shares_pay', 'treasury_shares_pay')
        read_only_fields = ('players', 'companies')

    def create(self, validated_data):
        game = models.Game.objects.create(**validated_data)
        entry = models.LogEntry.objects.create(game=game,
            text='New game started')
        game.log_cursor = entry
        game.save()
        return game


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Player
        fields = ('url', 'uuid', 'name', 'game', 'cash', 'shares', 'share_set')
        read_only_fields = ('shares', 'share_set')
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=models.Player.objects.all(),
                fields=('game', 'name'),
                message=DUPLICATE_PLAYER_ERROR,
            ),
        )

    def create(self, validated_data):
        player = models.Player.objects.create(**validated_data)
        game = player.game
        game.cash -= validated_data['cash']
        # Create log entry
        entry = models.LogEntry.objects.create(game=player.game,
            text='Added player {name} with {cash} starting cash'.format(
                name=validated_data['name'], cash=validated_data['cash']))
        game.log_cursor = entry
        game.save()
        return player


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = ('url', 'uuid', 'name', 'text_color', 'background_color',
            'game', 'cash', 'share_count', 'ipo_shares', 'bank_shares',
            'player_owners', 'share_set')
        read_only_fields = ('player_owners', 'share_set')
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=models.Company.objects.all(),
                fields=('game', 'name'),
                message=DUPLICATE_COMPANY_ERROR,
            ),
        )

    def create(self, validated_data):
        company = models.Company.objects.create(**validated_data)
        game = company.game
        game.cash -= validated_data['cash']
        entry = models.LogEntry.objects.create(game=game,
            text='Added {}-share company {} with {} starting cash'.format(
                validated_data['share_count'], validated_data['name'],
                validated_data['cash']),
            acting_company=company)
        game.log_cursor = entry
        game.save()
        return company

    def update(self, instance, validated_data):
        if instance.share_count != validated_data['share_count']:
            share_delta = validated_data['share_count'] - instance.share_count
            # Removing more shares then there are in the IPO
            if share_delta < -instance.ipo_shares:
                validated_data['ipo_shares'] = 0
                validated_data['bank_shares'] += share_delta + \
                    instance.ipo_shares
            else:
                validated_data['ipo_shares'] += share_delta
        return super(CompanySerializer, self).update(instance, validated_data)


class PlayerShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PlayerShare
        fields = ('url', 'uuid', 'owner', 'company', 'shares')


class CompanyShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyShare
        fields = ('url', 'uuid', 'owner', 'company', 'shares')


class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LogEntry
        fields = ('url', 'uuid', 'game', 'time', 'text', 'acting_company')


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
        return data

    @property
    def source_instance(self):
        if 'from_player' in self.validated_data.keys():
            return get_object_or_404(models.Player,
                uuid=self.validated_data['from_player'])
        if 'from_company' in self.validated_data.keys():
            return get_object_or_404(models.Company,
                uuid=self.validated_data['from_company'])
        return None

    @property
    def dest_instance(self):
        if 'to_player' in self.validated_data.keys():
            return get_object_or_404(models.Player,
                uuid=self.validated_data['to_player'])
        if 'to_company' in self.validated_data.keys():
            return get_object_or_404(models.Company,
                uuid=self.validated_data['to_company'])
        return None


class TransferShareSerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=False, default=1)
    price = serializers.IntegerField()
    share = serializers.ModelField(
        model_field=models.Company._meta.get_field('uuid'))

    buyer_type = serializers.ChoiceField(choices=['ipo', 'bank', 'player',
        'company'])
    player_buyer = serializers.ModelField(required=False,
        model_field=models.Player._meta.get_field('uuid'))
    company_buyer = serializers.ModelField(required=False,
        model_field=models.Player._meta.get_field('uuid'))

    source_type = serializers.ChoiceField(choices=['ipo', 'bank', 'player',
        'company'])
    player_source = serializers.ModelField(required=False,
        model_field=models.Player._meta.get_field('uuid'))
    company_source = serializers.ModelField(required=False,
        model_field=models.Player._meta.get_field('uuid'))

    def validate(self, data):
        if data['source_type'] == 'player' and \
                'player_source' not in data.keys():
            raise serializers.ValidationError(SOURCE_REQUIRED_ERROR)
        if data['source_type'] == 'company' and \
                'company_source' not in data.keys():
            raise serializers.ValidationError(SOURCE_REQUIRED_ERROR)
        if data['buyer_type'] == 'player' and \
                'player_buyer' not in data.keys():
            raise serializers.ValidationError(BUYER_REQUIRED_ERROR)
        if data['buyer_type'] == 'company' and \
                'company_buyer' not in data.keys():
            raise serializers.ValidationError(BUYER_REQUIRED_ERROR)
        return data


class OperateSerializer(serializers.Serializer):
    company = serializers.ModelField(
        model_field=models.Company._meta.get_field('uuid'))
    amount = serializers.IntegerField()
    method = serializers.ChoiceField(choices=['full', 'half', 'withhold'])
