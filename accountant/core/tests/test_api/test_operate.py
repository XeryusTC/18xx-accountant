# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest import mock

from ... import factories
from ... import utils

@mock.patch.object(utils, 'operate')
class OperateTests(APITestCase):
    def setUp(self):
        self.url = reverse('operate')
        self.company = factories.CompanyFactory()

    def test_GET_request_is_empty(self, mock):
        """GET is for debug (and doc) purposes only"""
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data)

    def test_company_can_pay_full_dividends(self, mock_operate):
        data = {'company': self.company.pk, 'amount': 10, 'method': 'full'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_operate.assert_called_once_with(self.company, 10,
            utils.OperateMethod.FULL)

    def test_company_can_pay_half_dividends(self, mock_operate):
        data = {'company': self.company.pk, 'amount': 20, 'method': 'half'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_operate.assert_called_once_with(self.company, 20,
            utils.OperateMethod.HALF)

    def test_company_can_withhold_revenue(self, mock_operate):
        data = {'company': self.company.pk, 'amount': 30, 'method': 'withhold'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_operate.assert_called_once_with(self.company, 30,
            utils.OperateMethod.WITHHOLD)

    def test_gives_error_if_request_is_invalid(self, mock_buy_share):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
