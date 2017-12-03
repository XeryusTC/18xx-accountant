# -*- coding: utf-8 -*-
from django.test import TestCase

from .. import factories
from .. import models
from .. import utils

class CreateLogEntryTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory(cash=0)
        self.alice, self.bob = factories.PlayerFactory.create_batch(size=2,
            game=self.game, cash=0)
        self.company, self.company2 = factories.CompanyFactory.create_batch(
            size=2, game=self.game, cash=0)

    def verify_entry(self, entry, action, amount=0, acting_player=None,
                     receiving_player=None, acting_company=None,
                     receiving_company=None, shares=0, price=0, buyer='',
                     player_buyer=None, company_buyer=None, source='',
                     player_source=None, company_source=None, company=None,
                     mode=None, revenue=0):
        self.assertEqual(entry.action, action)
        self.assertEqual(entry.amount, amount)
        self.assertEqual(entry.acting_player, acting_player)
        self.assertEqual(entry.receiving_player, receiving_player)
        self.assertEqual(entry.acting_company, acting_company)
        self.assertEqual(entry.receiving_company, receiving_company)
        self.assertEqual(entry.shares, shares)
        self.assertEqual(entry.price, price)
        self.assertEqual(entry.buyer, buyer)
        self.assertEqual(entry.player_buyer, player_buyer)
        self.assertEqual(entry.company_buyer, company_buyer)
        self.assertEqual(entry.source, source)
        self.assertEqual(entry.player_source, player_source)
        self.assertEqual(entry.company_source, company_source)
        self.assertEqual(entry.company, company)
        self.assertEqual(entry.mode, mode)

    def test_money_transfer_from_player_to_bank_creates_log_entry(self):
        utils.create_log_entry(self.game, models.LogEntry.TRANSFER_MONEY,
            amount=1, acting=self.alice)
        self.game.refresh_from_db()
        self.verify_entry(self.game.log_cursor, models.LogEntry.TRANSFER_MONEY,
            acting_player=self.alice, amount=1)

    def test_money_transfer_from_player_to_player_creates_log_entry(self):
        utils.create_log_entry(self.game, models.LogEntry.TRANSFER_MONEY,
            amount=2, acting=self.alice, receiving=self.bob)
        self.game.refresh_from_db()
        self.verify_entry(self.game.log_cursor, models.LogEntry.TRANSFER_MONEY,
            acting_player=self.alice, receiving_player=self.bob, amount=2)

    def test_money_transfer_from_player_to_company_creates_log_entry(self):
        utils.create_log_entry(self.game, models.LogEntry.TRANSFER_MONEY,
            amount=3, acting=self.alice,
            receiving=self.company)
        self.game.refresh_from_db()
        self.verify_entry(self.game.log_cursor, models.LogEntry.TRANSFER_MONEY,
            acting_player=self.alice, receiving_company=self.company, amount=3)

    def test_money_transfer_from_company_to_bank_creates_log_entry(self):
        utils.create_log_entry(self.game, models.LogEntry.TRANSFER_MONEY,
            amount=4, acting=self.company)
        self.game.refresh_from_db()
        self.verify_entry(self.game.log_cursor, models.LogEntry.TRANSFER_MONEY,
            acting_company=self.company, amount=4)

    def test_money_transfer_from_company_to_player_creates_log_entry(self):
        utils.create_log_entry(self.game, models.LogEntry.TRANSFER_MONEY,
            amount=5, acting=self.company, receiving=self.bob)
        self.game.refresh_from_db()
        self.verify_entry(self.game.log_cursor, models.LogEntry.TRANSFER_MONEY,
            acting_company=self.company, receiving_player=self.bob, amount=5)

    def test_money_transfer_from_company_to_company_creates_log_entry(self):
        utils.create_log_entry(self.game, models.LogEntry.TRANSFER_MONEY,
            amount=6, acting=self.company, receiving=self.company2)
        self.game.refresh_from_db()
        self.verify_entry(self.game.log_cursor, models.LogEntry.TRANSFER_MONEY,
            acting_company=self.company, receiving_company=self.company2,
            amount=6)

    def test_player_transfering_share_from_ipo_creates_log_entry(self):
        utils.create_log_entry(self.game, models.LogEntry.TRANSFER_SHARE,
            shares=7, price=8, buyer=self.alice, source=utils.Share.IPO,
            company=self.company)
        self.game.refresh_from_db()
        self.verify_entry(self.game.log_cursor, models.LogEntry.TRANSFER_SHARE,
            shares=7, price=8, buyer='player', player_buyer=self.alice,
            source='ipo', company=self.company)

    def test_player_transfering_share_from_bank_creates_log_entry(self):
        utils.create_log_entry(self.game, models.LogEntry.TRANSFER_SHARE,
            shares=9, price=10, buyer=self.alice, source=utils.Share.BANK,
            company=self.company)
        self.game.refresh_from_db()
        self.verify_entry(self.game.log_cursor, models.LogEntry.TRANSFER_SHARE,
            shares=9, price=10, buyer='player', player_buyer=self.alice,
            source='bank', company=self.company)

    def test_player_transfering_share_from_player_creates_log_entry(self):
        utils.create_log_entry(self.game, models.LogEntry.TRANSFER_SHARE,
            shares=11, price=12, buyer=self.alice, source=self.bob,
            company=self.company)
        self.game.refresh_from_db()
        self.verify_entry(self.game.log_cursor, models.LogEntry.TRANSFER_SHARE,
            shares=11, price=12, buyer='player', player_buyer=self.alice,
            source='player', player_source=self.bob, company=self.company)

    def test_player_transfering_share_from_company_creates_log_entry(self):
        utils.create_log_entry(self.game, models.LogEntry.TRANSFER_SHARE,
            shares=13, price=14, buyer=self.alice, source=self.company2,
            company=self.company)
        self.game.refresh_from_db()
        self.verify_entry(self.game.log_cursor, models.LogEntry.TRANSFER_SHARE,
            shares=13, price=14, buyer='player', player_buyer=self.alice,
            source='company', company_source=self.company2,
            company=self.company)

    def test_company_transfering_share_from_ipo_creates_log_entry(self):
        utils.create_log_entry(self.game, models.LogEntry.TRANSFER_SHARE,
            shares=15, price=16, buyer=self.company2, source=utils.Share.IPO,
            company=self.company)
        self.game.refresh_from_db()
        self.verify_entry(self.game.log_cursor, models.LogEntry.TRANSFER_SHARE,
            shares=15, price=16, buyer='company', company_buyer=self.company2,
            source='ipo', company=self.company, acting_company=self.company2)

    def test_company_transfering_share_from_bank_creates_log_entry(self):
        utils.create_log_entry(self.game, models.LogEntry.TRANSFER_SHARE,
            shares=17, price=18, buyer=self.company2, source=utils.Share.BANK,
            company=self.company)
        self.game.refresh_from_db()
        self.verify_entry(self.game.log_cursor, models.LogEntry.TRANSFER_SHARE,
            shares=17, price=18, buyer='company', company_buyer=self.company2,
            source='bank', company=self.company, acting_company=self.company2)

    def test_company_transfering_share_from_player_creates_log_entry(self):
        utils.create_log_entry(self.game, models.LogEntry.TRANSFER_SHARE,
            shares=19, price=20, buyer=self.company2, source=self.alice,
            company=self.company)
        self.game.refresh_from_db()
        self.verify_entry(self.game.log_cursor, models.LogEntry.TRANSFER_SHARE,
            shares=19, price=20, buyer='company', company_buyer=self.company2,
            source='player', player_source=self.alice, company=self.company,
            acting_company=self.company2)

    def test_company_transfering_share_from_company_creates_log_entry(self):
        utils.create_log_entry(self.game, models.LogEntry.TRANSFER_SHARE,
            shares=21, price=22, buyer=self.company2, source=self.company,
            company=self.company)
        self.game.refresh_from_db()
        self.verify_entry(self.game.log_cursor, models.LogEntry.TRANSFER_SHARE,
            shares=21, price=22, buyer='company', company_buyer=self.company2,
            source='company', company_source=self.company,
            company=self.company, acting_company=self.company2)

    def test_company_paying_full_creates_log_entry(self):
        utils.create_log_entry(self.game, models.LogEntry.OPERATE,
            mode=models.LogEntry.FULL, amount=23, company=self.company)
        self.game.refresh_from_db()
        self.verify_entry(self.game.log_cursor, models.LogEntry.OPERATE,
            mode=models.LogEntry.FULL, amount=23,
            acting_company=self.company)

    def test_company_paying_half_creates_log_entry(self):
        utils.create_log_entry(self.game, models.LogEntry.OPERATE,
            mode=models.LogEntry.HALF, amount=24, company=self.company)
        self.game.refresh_from_db()
        self.verify_entry(self.game.log_cursor, models.LogEntry.OPERATE,
            mode=models.LogEntry.HALF, amount=24,
            acting_company=self.company)

    def test_company_withholding_creates_log_entry(self):
        utils.create_log_entry(self.game, models.LogEntry.OPERATE,
            mode=models.LogEntry.WITHHOLD, amount=25, company=self.company)
        self.game.refresh_from_db()
        self.verify_entry(self.game.log_cursor, models.LogEntry.OPERATE,
            mode=models.LogEntry.WITHHOLD, amount=25,
            acting_company=self.company)

    def test_clears_redo_stack_when_adding_new_entry(self):
        entry1 = models.LogEntry.objects.create(game=self.game)
        entry2 = models.LogEntry.objects.create(game=self.game)
        self.game.log_cursor = entry1
        self.game.save()

        entry3 = utils.create_log_entry(self.game, None)

        self.game.refresh_from_db()
        self.assertEqual(list(self.game.log.all()), [entry1, entry3])
        with self.assertRaises(models.LogEntry.DoesNotExist):
            entry2.refresh_from_db()
