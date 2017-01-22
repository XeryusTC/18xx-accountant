# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, serializers, utils

class GameViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the default methods and an additional 'create'
    view.
    """
    queryset = models.Game.objects.all()
    serializer_class = serializers.GameSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = models.Player.objects.all()
    serializer_class = serializers.PlayerSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer


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
            utils.transfer_money(serializer.source_instance,
                serializer.dest_instance, serializer.validated_data['amount'])
            return Response(serializer.validated_data,
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
