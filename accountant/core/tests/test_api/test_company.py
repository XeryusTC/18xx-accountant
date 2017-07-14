# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ... import models
from ... import factories

class CompanyTests(APITestCase):
    def setUp(self):
        self.game = factories.GameFactory()

    def test_create_company(self):
        """Ensure that we can create companies."""
        url = reverse('company-list')
        data = {'name': 'B&O', 'game': self.game.pk, 'cash': 100,
                'share_count': 100}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "Could not create a company: " + str(response.data))
        self.assertEqual(models.Company.objects.count(), 1)

    def test_cannot_create_duplicate_company_for_single_game(self):
        """Disallow creating two companies with the same name in a game."""
        factories.CompanyFactory.create(game=self.game, name='B&O')
        url = reverse('company-list')
        data = {'name': 'B&O', 'game': self.game.pk}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            "Created duplicate company: " + str(response.data))
        self.assertEqual(models.Company.objects.count(), 1)

    def test_creating_company_decreases_cash_in_bank(self):
        self.game.cash = 1000
        self.game.save()
        url = reverse('company-list')
        data = {'name': 'PRR', 'game': self.game.pk, 'cash': 300,
            'share_count': 10}

        response = self.client.post(url, data, format='json')

        self.game.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Company.objects.first().cash, 300)
        self.assertEqual(self.game.cash, 700)

    def test_retrieve_all_companies_when_no_query_params_set(self):
        factories.CompanyFactory.create_batch(size=5)
        url = reverse('company-list')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual([c.name for c in models.Company.objects.all()],
            [c['name'] for c in response.data])

    def test_retrieve_companies_within_a_single_game(self):
        """Filter companies based on the game in the query parameters"""
        companies = factories.CompanyFactory.create_batch(game=self.game,
            size=2)
        factories.CompanyFactory.create_batch(size=2)
        url = reverse('company-list') + '?game=' + str(self.game.pk)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual([c.name for c in companies],
            [c['name'] for c in response.data])

    def test_creating_company_adds_log_entry(self):
        url = reverse('company-list')
        data = {'name': 'Erie', 'game': self.game.pk, 'cash': 500,
                'share_count': 5}

        response = self.client.post(url, data, format='json')

        self.game.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(2,
            models.LogEntry.objects.filter(game=self.game).count())
        self.assertEqual(self.game.log.last().text,
            'Added 5-share company Erie with 500 starting cash')
        self.assertEqual(self.game.log_cursor, self.game.log.last())


class CompanyShareTests(APITestCase):
    def setUp(self):
        self.game = factories.GameFactory()

    def test_create_self_owning_share(self):
        """Ensure that we can create company shares."""
        company = factories.CompanyFactory.create(game=self.game)
        url = reverse('companyshare-list')
        data = {'owner': company.pk, 'company': company.pk}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "Could not create a self owning share: " + str(response.data))
        self.assertEqual(models.CompanyShare.objects.count(), 1)

    def test_create_share_owning_other_company(self):
        """Ensure that companies can own shares in other companies."""
        company1, company2 = factories.CompanyFactory.create_batch(size=2,
            game=self.game)
        url = reverse('companyshare-list')
        data = {'owner': company1.pk, 'company': company2.pk}

        response = self.client.post(url, data, format='json')

        share = models.CompanyShare.objects.first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "Could not create a company share: " + str(response.data))
        self.assertEqual(models.CompanyShare.objects.count(), 1)
        self.assertEqual(share.owner, company1)
        self.assertEqual(share.company, company2)

    def test_cannot_create_duplicate_share_holdings(self):
        """
        Ensure that a company doesn't have two share holding records for a
        single company
        """
        company1, company2 = factories.CompanyFactory.create_batch(size=2,
            game=self.game)
        factories.CompanyShareFactory.create(owner=company1,
            company=company2)
        url = reverse('companyshare-list')
        data = {'owner': company1.pk, 'company': company2.pk}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            "Created duplicate share holdings: " + str(response.data))
        self.assertEqual(models.CompanyShare.objects.count(), 1)
        self.assertIn('non_field_errors', response.data.keys())

    def test_retrieve_all_shares_when_no_query_params_set(self):
        factories.CompanyShareFactory.create_batch(size=7)
        url = reverse('companyshare-list')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual([s['uuid'] for s in response.data],
            [str(s.uuid) for s in models.CompanyShare.objects.all()])

    def test_retrieve_shares_of_single_company(self):
        company = factories.CompanyFactory.create()
        shares = factories.CompanyShareFactory.create_batch(owner=company,
            size=3)
        factories.CompanyShareFactory.create_batch(size=5)
        url = reverse('companyshare-list') + '?owner=' + str(company.pk)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual([s['uuid'] for s in response.data],
            [str(s.uuid) for s in shares])

    def test_retrieve_all_shares_in_a_game(self):
        companies = factories.CompanyFactory.create_batch(game=self.game,
            size=2)
        shares = factories.CompanyShareFactory.create_batch(size=2,
            owner=companies[0]) + factories.CompanyShareFactory.create_batch(
                size=3, owner=companies[1])
        factories.CompanyShareFactory.create_batch(size=5)
        url = reverse('companyshare-list') + '?game=' + str(self.game.pk)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual([s['uuid'] for s in response.data],
            [str(s.uuid) for s in shares])
