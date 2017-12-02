# -*- coding: utf-8 -*-
from django.test import TestCase
from unittest import mock

from .. import factories
from .. import models
from .. import utils

@mock.patch.object(utils, 'operate')
class UndoOperateTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory(cash=1000)
        self.start_entry = models.LogEntry.objects.create(game=self.game,
            text='New game')
        self.game.log_cursor = self.start_entry
        self.game.save()
        self.alice, self.bob, self.dave = factories.PlayerFactory.create_batch(
            game=self.game, size=3)
        self.company, self.company2 = factories.CompanyFactory.create_batch(
            game=self.game, size=2)
        factories.PlayerShareFactory(owner=self.alice, company=self.company,
            shares=3)
        factories.PlayerShareFactory(owner=self.bob, company=self.company,
            shares=2)
        factories.CompanyShareFactory(owner=self.company2,
            company=self.company, shares=1)

    def create_entry(self, **kwargs):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.OPERATE, company=self.company, **kwargs)
        self.game.log_cursor = entry
        self.game.save()

    def test_can_undo_company_operating_full(self, mock_operate):
        self.create_entry(mode=models.LogEntry.FULL, revenue=10)
        utils.undo(self.game)
        mock_operate.assert_called_once_with(self.company, -10,
            utils.OperateMethod.FULL)

    def test_can_undo_company_operating_half(self, mock_operate):
        self.create_entry(mode=models.LogEntry.HALF, revenue=20)
        utils.undo(self.game)
        mock_operate.assert_called_once_with(self.company, -20,
            utils.OperateMethod.HALF)

    def test_can_undo_company_withholding(self, mock_operate):
        self.create_entry(mode=models.LogEntry.WITHHOLD, revenue=30)
        utils.undo(self.game)
        mock_operate.assert_called_once_with(self.company, -30,
            utils.OperateMethod.WITHHOLD)

    def test_undoing_company_operating_full_returns_affected(self, mock):
        self.create_entry(mode=models.LogEntry.FULL, revenue=40)
        affected = utils.undo(self.game)
        self.assertEqual(affected['game'], self.game)
        self.assertCountEqual(affected['players'], [self.alice, self.bob])
        self.assertEqual(list(affected['companies']), [self.company2])

    def test_undoing_company_operating_half_returns_affected(self, mock):
        self.create_entry(mode=models.LogEntry.HALF, revenue=50)
        affected = utils.undo(self.game)
        self.assertEqual(affected['game'], self.game)
        self.assertCountEqual(affected['players'], [self.alice, self.bob])
        self.assertCountEqual(affected['companies'],
            [self.company, self.company2])

    def test_undoing_company_withholding_returns_affected(self, mock):
        self.create_entry(mode=models.LogEntry.WITHHOLD, revenue=60)
        affected = utils.undo(self.game)
        self.assertEqual(affected['game'], self.game)
        self.assertNotIn('players', affected.keys())
        self.assertEqual(list(affected['companies']), [self.company])
