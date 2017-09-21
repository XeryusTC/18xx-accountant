# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, serializers, utils

NO_AVAILABLE_SHARES_ERROR = _("Source doesn't have enough shares to sell")
DIFFERENT_GAME_ERROR = \
    _("The transaction is not between individuals in the same game")

class GameViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the default methods and an additional 'create'
    view.
    """
    queryset = models.Game.objects.all()
    serializer_class = serializers.GameSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PlayerSerializer

    def get_queryset(self):
        game_uuid = self.request.query_params.get('game', None)
        if game_uuid is not None:
            queryset = models.Player.objects.filter(game=game_uuid)
        else:
            queryset = models.Player.objects.all()
        return queryset


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CompanySerializer

    def get_queryset(self):
        game_uuid = self.request.query_params.get('game', None)
        if game_uuid is not None:
            queryset = models.Company.objects.filter(game=game_uuid)
        else:
            queryset = models.Company.objects.all()
        return queryset


class PlayerShareViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PlayerShareSerializer

    def get_queryset(self):
        player_uuid = self.request.query_params.get('owner', None)
        game_uuid = self.request.query_params.get('game', None)
        if player_uuid is not None:
            return models.PlayerShare.objects.filter(owner=player_uuid)
        if game_uuid is not None:
            return models.PlayerShare.objects.filter(owner__game=game_uuid)
        return models.PlayerShare.objects.all()


class CompanyShareViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CompanyShareSerializer

    def get_queryset(self):
        company_uuid = self.request.query_params.get('owner', None)
        game_uuid = self.request.query_params.get('game', None)
        if company_uuid is not None:
            return models.CompanyShare.objects.filter(owner=company_uuid)
        if game_uuid is not None:
            return models.CompanyShare.objects.filter(owner__game=game_uuid)
        return models.CompanyShare.objects.all()


class LogEntryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.LogEntrySerializer

    def get_queryset(self):
        game_uuid = self.request.query_params.get('game', None)
        if game_uuid is not None:
            queryset = models.LogEntry.objects.filter(game=game_uuid)
        else:
            queryset = models.LogEntry.objects.all()
        return queryset


class TransferMoneyView(APIView):
    serializer_class = serializers.TransferMoneySerializer

    def get(self, request, format=None):
        return Response()

    def post(self, request, format=None):
        serializer = serializers.TransferMoneySerializer(data=request.data)
        if serializer.is_valid():
            # Check if the transfer is valid (within same game)
            if serializer.source_instance != None \
                    and serializer.dest_instance != None \
                    and serializer.source_instance.game != \
                        serializer.dest_instance.game:  # noqa
                return Response(
                    {'non_field_errors': serializers.DIFFERENT_GAME_ERROR},
                    status=status.HTTP_400_BAD_REQUEST)
            # Do the transfering
            utils.transfer_money(serializer.source_instance,
                serializer.dest_instance, serializer.validated_data['amount'])
            # Create the log entry
            if serializer.source_instance != None:
                game = serializer.source_instance.game
                source_name = serializer.source_instance.name
            else:
                game = serializer.dest_instance.game
                source_name = 'The bank'
            if serializer.dest_instance != None:
                dest_name = serializer.dest_instance.name
            else:
                dest_name = 'the bank'
            entry = models.LogEntry.objects.create(game=game,
                amount=serializer.validated_data['amount'],
                text='{source} transfered {cash} to {dest}'.format(
                    source=source_name, dest=dest_name,
                    cash=serializer.validated_data['amount']),
                action=models.LogEntry.TRANSFER_MONEY)
            if isinstance(serializer.source_instance, models.Player):
                entry.acting_player = serializer.source_instance
            elif isinstance(serializer.source_instance, models.Company):
                entry.acting_company = serializer.source_instance
            entry.save()
            game.log_cursor = entry
            game.save()

            # Construct the response, starting with the game
            context = {'request': self.request}
            res = {}
            if (serializer.source_instance == None or
                    serializer.dest_instance == None):
                res['game'] = serializers.GameSerializer(game,
                    context=context).data
            # Add the log entry
            res['log'] = serializers.LogEntrySerializer(entry,
                context=context).data
            # Next do players
            players = []
            if isinstance(serializer.source_instance, models.Player):
                players.append(serializers.PlayerSerializer(
                    serializer.source_instance, context=context).data)
            if isinstance(serializer.dest_instance, models.Player):
                players.append(serializers.PlayerSerializer(
                    serializer.dest_instance, context=context).data)
            if players:
                res['players'] = players
            # Finally do companies
            companies = []
            if isinstance(serializer.source_instance, models.Company):
                companies.append(serializers.CompanySerializer(
                    serializer.source_instance, context=context).data)
            if isinstance(serializer.dest_instance, models.Company):
                companies.append(serializers.CompanySerializer(
                    serializer.dest_instance, context=context).data)
            if companies:
                res['companies'] = companies

            return Response(res, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransferShareView(APIView):
    serializer_class = serializers.TransferShareSerializer

    def get(self, request, format=None):
        return Response()

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # determine buyer
            buyer_name = None
            if serializer.validated_data['buyer_type'] == 'ipo':
                buyer = utils.Share.IPO
            elif serializer.validated_data['buyer_type'] == 'bank':
                buyer = utils.Share.BANK
            elif serializer.validated_data['buyer_type'] == 'player':
                buyer = models.Player.objects.get(
                    pk=serializer.validated_data['player_buyer'])
                buyer_name = buyer.name
            elif serializer.validated_data['buyer_type'] == 'company':
                buyer = models.Company.objects.get(
                    pk=serializer.validated_data['company_buyer'])
                buyer_name = buyer.name

            # determine source
            if serializer.validated_data['source_type'] == 'ipo':
                source = utils.Share.IPO
                source_name = 'the IPO'
            elif serializer.validated_data['source_type'] == 'bank':
                source = utils.Share.BANK
                source_name = 'the bank'
            elif serializer.validated_data['source_type'] == 'player':
                source = models.Player.objects.get(
                    pk=serializer.validated_data['player_source'])
                source_name = source.name
            elif serializer.validated_data['source_type'] == 'company':
                source = models.Company.objects.get(
                    pk=serializer.validated_data['company_source'])
                source_name = source.name

            # determine which company is being bought/sold
            share = models.Company.objects.get(
                pk=serializer.validated_data['share'])
            # Get amount of shares being bought/sold
            amount = serializer.validated_data['amount']
            # buy/sell the share
            price = serializer.validated_data['price']
            try:
                utils.buy_share(buyer, share, source, price, amount)
            except utils.DifferentGameException:
                return Response({'non_field_errors': [DIFFERENT_GAME_ERROR]},
                    status=status.HTTP_400_BAD_REQUEST)
            except utils.InvalidShareTransaction:
                return Response(
                    {'non_field_errors': [NO_AVAILABLE_SHARES_ERROR]},
                    status=status.HTTP_400_BAD_REQUEST)

            # create log entry
            if amount > 0:
                log_string = '{buyer} bought {amount} shares {company} ' + \
                             'from {source} for {price} each'
            else:
                log_string = '{buyer} sold {amount} shares {company} ' + \
                             'to {source} for {price} each'
            entry = models.LogEntry.objects.create(game=share.game,
                text=log_string.format(buyer=buyer_name, amount=abs(amount),
                                       company=share.name, source=source_name,
                                       price=price))
            if isinstance(buyer, models.Company):
                entry.acting_company = buyer
                entry.save()
            share.game.refresh_from_db()
            share.game.log_cursor = entry
            share.game.save()

            # Construct the response, starting with the game
            context = {'request': request}
            response = {}
            if (buyer == utils.Share.IPO or buyer == utils.Share.BANK or
                    source == utils.Share.IPO or source == utils.Share.BANK):
                response['game'] = serializers.GameSerializer(
                    share.game, context=context).data
            # Add the log entry
            response['log'] = serializers.LogEntrySerializer(entry,
                context=context).data
            # Add players next
            players = []
            if isinstance(buyer, models.Player):
                players.append(serializers.PlayerSerializer(buyer,
                    context=context).data)
            if isinstance(source, models.Player):
                players.append(serializers.PlayerSerializer(source,
                    context=context).data)
            if players:
                response['players'] = players
            # Add companies
            companies = [serializers.CompanySerializer(share, context=context)
                    .data]
            if isinstance(buyer, models.Company) and buyer != share:
                companies.append(serializers.CompanySerializer(buyer,
                    context=context).data)
            if isinstance(source, models.Company) and source != share:
                companies.append(serializers.CompanySerializer(source,
                    context=context).data)
            response['companies'] = companies
            # Add the share holding records
            shares = []
            if isinstance(buyer, models.Player):
                shares.append(serializers.PlayerShareSerializer(
                    buyer.share_set.get(company=share), context=context).data)
            if isinstance(buyer, models.Company):
                shares.append(serializers.CompanyShareSerializer(
                    buyer.share_set.get(company=share), context=context).data)
            if isinstance(source, models.Player):
                shares.append(serializers.PlayerShareSerializer(
                    source.share_set.get(company=share), context=context).data)
            if isinstance(source, models.Company):
                shares.append(serializers.CompanyShareSerializer(
                    source.share_set.get(company=share), context=context).data)
            response['shares'] = shares

            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OperateView(APIView):
    serializer_class = serializers.OperateSerializer

    def get(self, request, format=None):
        return Response()

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            if serializer.validated_data['method'] == 'full':
                method = utils.OperateMethod.FULL
                log_text = '{company} operates for {amount} which is paid ' + \
                           'as dividends'
            elif serializer.validated_data['method'] == 'half':
                method = utils.OperateMethod.HALF
                log_text = '{company} operates for {amount} of which it ' + \
                           'retains half'
            elif serializer.validated_data['method'] == 'withhold':
                method = utils.OperateMethod.WITHHOLD
                log_text = '{company} withholds {amount}'

            company = models.Company.objects.get(
                pk=serializer.validated_data['company'])
            affected = utils.operate(company, amount, method)

            company.refresh_from_db()
            company.game.refresh_from_db()

            # Create log entry
            entry = models.LogEntry.objects.create(game=company.game,
                text=log_text.format(company=company.name, amount=amount),
                acting_company=company)
            company.game.log_cursor = entry
            company.game.save()

            # Construct response
            context = {'request': request}
            response = {
                'companies': [],
                'game': serializers.GameSerializer(company.game,
                    context=context).data,
                'log': serializers.LogEntrySerializer(entry,
                    context=context).data
            }
            for entity, amount in affected.items():
                if isinstance(entity, models.Player):
                    if 'players' not in response:
                        response['players'] = []
                    response['players'].append(serializers.PlayerSerializer(
                        entity, context=context).data)
                elif isinstance(entity, models.Company):
                    response['companies'].append(serializers.CompanySerializer(
                        entity, context=context).data)

            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ColorsView(APIView):
    def get(self, request, format=None):
        return Response(models.Company.COLOR_CODES)


class UndoRedoView(APIView):
    serializer_class = serializers.UndoRedoSerializer

    def get(self, request, format=None):
        return Response()

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['action'] == 'undo':
                func = utils.undo
            else:
                func = utils.redo
            affected = func(models.Game.objects.get(
                pk=serializer.validated_data['game']))

            # Construct response
            context = {'request': request}
            response = {
                'game': serializers.GameSerializer(affected['game'],
                    context=context).data,
            }
            if 'players' in affected:
                response['players'] = []
                for player in affected['players']:
                    response['players'].append(serializers.PlayerSerializer(
                        player, context=context).data)
            if 'log' in affected:
                response['log'] = serializers.LogEntrySerializer(
                    affected['log'], context=context).data

            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
