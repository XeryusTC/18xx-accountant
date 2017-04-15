# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, serializers, utils

NO_AVAILABLE_SHARES_ERROR = _("Source doesn't have enough shares to sell")

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
    queryset = models.PlayerShare.objects.all()
    serializer_class = serializers.PlayerShareSerializer


class CompanyShareViewSet(viewsets.ModelViewSet):
    queryset = models.CompanyShare.objects.all()
    serializer_class = serializers.CompanyShareSerializer


class TransferMoneyView(APIView):
    serializer_class = serializers.TransferMoneySerializer

    def get(self, request, format=None):
        return Response()

    def post(self, request, format=None):
        serializer = serializers.TransferMoneySerializer(data=request.data)
        if serializer.is_valid():
            if serializer.source_instance != None \
                    and serializer.dest_instance != None \
                    and serializer.source_instance.game != \
                        serializer.dest_instance.game:
                return Response(
                    {'non_field_errors': serializers.DIFFERENT_GAME_ERROR},
                    status=status.HTTP_400_BAD_REQUEST)
            utils.transfer_money(serializer.source_instance,
                serializer.dest_instance, serializer.validated_data['amount'])
            return Response(serializer.validated_data,
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransferShareView(APIView):
    serializer_class = serializers.TransferShareSerializer

    def get(self, request, format=None):
        return Response()

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # determine buyer
            if serializer.validated_data['buyer_type'] == 'ipo':
                buyer = utils.Share.IPO
            elif serializer.validated_data['buyer_type'] == 'bank':
                buyer = utils.Share.BANK
            elif serializer.validated_data['buyer_type'] == 'player':
                buyer = models.Player.objects.get(
                    pk=serializer.validated_data['player_buyer'])
            elif serializer.validated_data['buyer_type'] == 'company':
                buyer = models.Company.objects.get(
                    pk=serializer.validated_data['company_buyer'])

            # determine source
            if serializer.validated_data['source_type'] == 'ipo':
                source = utils.Share.IPO
            elif serializer.validated_data['source_type'] == 'bank':
                source = utils.Share.BANK
            elif serializer.validated_data['source_type'] == 'player':
                source = models.Player.objects.get(
                    pk=serializer.validated_data['player_source'])
            elif serializer.validated_data['source_type'] == 'company':
                source = models.Company.objects.get(
                    pk=serializer.validated_data['company_source'])

            # determine which company is being bought/sold
            share = models.Company.objects.get(
                pk=serializer.validated_data['share'])
            # turn negative shares into sell action
            amount = serializer.validated_data['amount']
            if amount < 0:
                buyer, source = source, buyer
                amount = -amount
            # buy/sell the share
            try:
                utils.buy_share(buyer, share, source,
                    serializer.validated_data['price'], amount)
            except:
                return Response(
                    {'non_field_errors': [NO_AVAILABLE_SHARES_ERROR]},
                    status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.validated_data,
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OperateView(APIView):
    serializer_class = serializers.OperateSerializer

    def get(self, request, format=None):
        return Response()

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['method'] == 'full':
                method = utils.OperateMethod.FULL
            elif serializer.validated_data['method'] == 'half':
                method = utils.OperateMethod.HALF
            elif serializer.validated_data['method'] == 'withhold':
                method = utils.OperateMethod.WITHHOLD

            company = models.Company.objects.get(
                pk=serializer.validated_data['company'])
            utils.operate(company, serializer.validated_data['amount'], method)
            return Response(serializer.validated_data,
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ColorsView(APIView):
    def get(self, request, format=None):
        return Response(models.Company.COLOR_CODES)
