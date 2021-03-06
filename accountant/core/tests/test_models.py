# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone
import uuid

from .. import factories
from ..models import Game, Player, Company, PlayerShare, CompanyShare, LogEntry

class GameTests(TestCase):
    def test_pk_is_uuid(self):
        game = Game()
        game.save()
        self.assertIsInstance(game.pk, uuid.UUID)

    def test_bank_cash_is_12000_by_default(self):
        game = Game()
        self.assertEqual(game.cash, 12000)

    def test_pool_shares_dont_pay_to_company_by_default(self):
        game = Game()
        self.assertFalse(game.pool_shares_pay)

    def test_ipo_shares_dont_pay_to_company_by_default(self):
        game = Game()
        self.assertFalse(game.ipo_shares_pay)

    def test_treasury_shares_pay_to_company_by_default(self):
        game = Game()
        self.assertTrue(game.treasury_shares_pay)

    def test_log_cursor_can_point_to_log_entries(self):
        game = Game.objects.create()
        entry = LogEntry.objects.create(game=game)
        game.log_cursor = entry
        game.save()

    def test_no_log_entry_when_creating_new_game(self):
        game = Game.objects.create()
        self.assertEqual(LogEntry.objects.filter(game=game).count(), 0)

    def test_log_cursor_is_None_by_default(self):
        game = Game.objects.create()
        self.assertIsNone(game.log_cursor)

    def test_string_representation(self):
        game = Game()
        self.assertIn('Game', str(game))
        self.assertIn(str(game.pk), str(game))


class PlayerTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory.create()

    def test_pk_is_uuid(self):
        player = Player(game=self.game)
        player.save()
        self.assertIsInstance(player.pk, uuid.UUID)

    def test_default_name(self):
        player = Player()
        self.assertEqual(player.name, 'Player')

    def test_cannot_create_duplicate_players_in_the_same_game(self):
        factories.PlayerFactory.create(name='Alice', game=self.game)
        player = Player(name='Alice', game=self.game)
        with self.assertRaises(IntegrityError):
            player.save()

    def test_can_create_players_with_different_name_in_the_same_game(self):
        factories.PlayerFactory.create(name='Alice', game=self.game)
        player = Player(name='Bob', game=self.game)
        player.save()

    def test_game_required(self):
        player = Player()
        with self.assertRaises(IntegrityError):
            player.save()

    def test_player_has_no_cash_by_default(self):
        player = Player()
        self.assertEqual(player.cash, 0)

    def test_player_returns_associated_game_instance(self):
        player = Player(game=self.game)
        self.assertEqual(player.game, self.game)

    def test_game_can_access_player_list(self):
        player = Player(game=self.game)
        player.save()
        self.assertEqual(list(self.game.players.all()), [player])

    def test_string_representation(self):
        player = Player(game=self.game, name='Alice')
        self.assertEqual('Alice', str(player))


class CompanyTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory.create()

    def test_pk_is_uuid(self):
        company = Company(game=self.game)
        company.save()
        self.assertIsInstance(company.pk, uuid.UUID)

    def test_default_name(self):
        company = Company()
        self.assertEqual(company.name, 'Company')

    def test_cannot_create_duplicate_companies_in_the_same_game(self):
        factories.CompanyFactory.create(name='B&O', game=self.game)
        company = Company(name='B&O', game=self.game)
        with self.assertRaises(IntegrityError):
            company.save()

    def test_can_create_companies_with_different_name_in_the_same_game(self):
        factories.CompanyFactory.create(name='B&O', game=self.game)
        company = Company(name='C&O', game=self.game)
        company.save()

    def test_can_create_same_company_for_different_game(self):
        game2 = factories.GameFactory.create()
        Company.objects.create(name='B&O', game=self.game)
        Company.objects.create(name='B&O', game=game2)

    def test_game_required(self):
        company = Company()
        with self.assertRaises(IntegrityError):
            company.save()

    def test_company_has_no_cash_by_default(self):
        company = Company()
        self.assertEqual(company.cash, 0)

    def test_company_returns_associated_game_instance(self):
        company = Company(game=self.game)
        self.assertEqual(company.game, self.game)

    def test_game_can_access_company_list(self):
        company = Company(game=self.game)
        company.save()
        self.assertEqual(list(self.game.companies.all()), [company])

    def test_has_text_color(self):
        Company(text_color='blue-500')

    def test_default_text_color_is_black(self):
        company = Company(game=self.game)
        self.assertEqual(company.text_color, 'black')

    def test_has_background_color(self):
        Company(background_color='white')

    def test_default_background_color_is_white(self):
        company = Company(game=self.game)
        self.assertEqual(company.background_color, 'white')

    def test_has_ten_shares_by_default(self):
        company = Company(game=self.game)
        self.assertEqual(company.share_count, 10)

    def test_shares_are_in_ipo_by_default(self):
        company = Company.objects.create(game=self.game)
        self.assertEqual(company.ipo_shares, 10)

    def test_number_of_ipo_shares_adjust_to_total_shares(self):
        company = Company.objects.create(game=self.game, share_count=5)
        company.refresh_from_db()
        self.assertEqual(company.ipo_shares, 5)

    def test_can_set_ipo_shares_to_be_zero(self):
        company = Company.objects.create(game=self.game, ipo_shares=0)
        company.refresh_from_db()
        self.assertEqual(company.ipo_shares, 0)

    def test_no_shares_in_bank_by_default(self):
        company = Company(game=self.game)
        self.assertEqual(company.bank_shares, 0)

    def test_string_representation(self):
        company = Company(game=self.game, name='B&O')
        self.assertEqual('B&O', str(company))


class PlayerShareTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory.create()
        self.player = factories.PlayerFactory.create(game=self.game)
        self.company = factories.CompanyFactory.create(game=self.game)

    def test_pk_is_uuid(self):
        share = PlayerShare.objects.create(owner=self.player,
            company=self.company)
        self.assertIsInstance(share.pk, uuid.UUID)

    def test_company_knows_about_owning_players(self):
        players = factories.PlayerFactory.create_batch(size=2, game=self.game)
        list(PlayerShare.objects.create(owner=p, company=self.company)
            for p in players)
        self.assertSequenceEqual(list(self.company.player_owners.all()),
            players)

    def test_player_with_no_shares_is_not_in_company_owners_list(self):
        players = factories.PlayerFactory.create_batch(size=2, game=self.game)
        PlayerShare.objects.create(owner=players[0], company=self.company)
        self.assertSequenceEqual(list(self.company.player_owners.all()),
            [players[0]])

    def test_player_knows_about_company_it_owns(self):
        PlayerShare.objects.create(owner=self.player, company=self.company)
        self.assertIn(self.company, list(self.player.shares.all()))

    def test_player_owns_one_share_by_default(self):
        factories.PlayerFactory.create(game=self.game)
        share = PlayerShare(owner=self.player, company=self.company)
        self.assertEqual(share.shares, 1)

    def test_game_is_equal_to_company_game(self):
        share = PlayerShare(owner=self.player, company=self.company)
        self.assertEqual(self.company.game, share.game)

    def test_cannot_create_duplicate_share_holdings(self):
        PlayerShare.objects.create(owner=self.player, company=self.company)
        with self.assertRaises(IntegrityError):
            PlayerShare.objects.create(owner=self.player,
                company=self.company)


class CompanyShareTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory.create()
        self.company1, self.company2 = factories.CompanyFactory.create_batch(
            size=2, game=self.game)

    def test_pk_is_uuid(self):
        share = CompanyShare.objects.create(owner=self.company1,
            company=self.company2)
        self.assertIsInstance(share.pk, uuid.UUID)

    def test_company_knows_about_owning_companies(self):
        CompanyShare.objects.create(owner=self.company1, company=self.company2)
        self.assertSequenceEqual(list(self.company2.company_owners.all()),
            [self.company1])

    def test_company_with_no_shares_is_not_in_company_owners_list(self):
        companies = factories.CompanyFactory.create_batch(size=2,
            game=self.game)
        CompanyShare.objects.create(owner=companies[0], company=self.company1)
        self.assertSequenceEqual([companies[0]],
            list(self.company1.company_owners.all()))

    def test_company_knows_about_companies_it_owns(self):
        CompanyShare.objects.create(owner=self.company1, company=self.company2)
        self.assertIn(self.company2, list(self.company1.shares.all()))

    def test_company_owns_one_share_by_default(self):
        share = CompanyShare(owner=self.company1, company=self.company2)
        self.assertEqual(share.shares, 1)

    def test_game_is_equal_to_company_game(self):
        share = CompanyShare(owner=self.company1, company=self.company2)
        self.assertEqual(self.company2.game, share.game)

    def test_cannot_create_duplicate_share_holdings(self):
        CompanyShare.objects.create(owner=self.company1, company=self.company2)
        with self.assertRaises(IntegrityError):
            CompanyShare.objects.create(owner=self.company1,
                company=self.company2)

    def test_company_can_own_its_own_shares(self):
        CompanyShare.objects.create(owner=self.company1, company=self.company1)


class LogEntryTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory.create()
        self.player = factories.PlayerFactory(game=self.game)
        self.company = factories.CompanyFactory.create(game=self.game)
        self.entry = LogEntry.objects.create(game=self.game)

    def test_pk_is_uuid(self):
        entry = LogEntry.objects.create(game=self.game)
        self.assertIsInstance(entry.pk, uuid.UUID)

    def test_game_required(self):
        entry = LogEntry()
        with self.assertRaises(IntegrityError):
            entry.save()

    def test_has_time_field(self):
        self.entry.time

    def test_text_is_empty_by_default(self):
        self.assertEqual(self.entry.text, '')

    def test_time_field_is_set_to_current_time(self):
        time = timezone.now()
        self.assertAlmostEqual(self.entry.time, time,
            delta=timedelta(seconds=5))

    def test_action_field_is_None_by_default(self):
        self.assertIsNone(self.entry.action)

    def test_action_field_can_be_TRANSFER_MONEY(self):
        LogEntry.objects.create(game=self.game, action=LogEntry.TRANSFER_MONEY)

    def test_action_field_can_be_TRANSFER_SHARE(self):
        LogEntry.objects.create(game=self.game, action=LogEntry.TRANSFER_SHARE)

    def test_action_field_can_be_OPERATE(self):
        LogEntry.objects.create(game=self.game, action=LogEntry.OPERATE)

    def test_acting_player_field_is_None_by_default(self):
        self.assertIsNone(self.entry.acting_player)

    def test_acting_player_field_points_to_player(self):
        LogEntry.objects.create(game=self.game, acting_player=self.player)

    def test_acting_company_field_is_None_by_default(self):
        self.assertIsNone(self.entry.acting_company)

    def test_acting_company_field_points_to_company(self):
        LogEntry.objects.create(game=self.game, acting_company=self.company)

    def test_receiving_player_field_is_None_by_default(self):
        self.assertIsNone(self.entry.receiving_player)

    def test_receiving_player_field_points_to_Player(self):
        LogEntry.objects.create(game=self.game, receiving_player=self.player)

    def test_receiving_company_field_is_None_by_default(self):
        self.assertIsNone(self.entry.receiving_company)

    def test_receiving_company_field_points_to_Company(self):
        LogEntry.objects.create(game=self.game, receiving_company=self.company)

    def test_amount_field_is_0_by_default(self):
        self.assertEquals(self.entry.amount, 0)

    def test_buyer_field_is_empty_by_default(self):
        self.assertEqual(self.entry.buyer, '')

    def test_source_field_is_empty_by_default(self):
        self.assertEqual(self.entry.source, '')

    def test_player_buyer_field_is_None_by_default(self):
        self.assertIsNone(self.entry.player_buyer)

    def test_player_buyer_field_points_to_Player(self):
        LogEntry.objects.create(game=self.game, player_buyer=self.player)

    def test_company_buyer_field_is_None_by_default(self):
        self.assertIsNone(self.entry.company_buyer)

    def test_company_buyer_field_points_to_company(self):
        LogEntry.objects.create(game=self.game, company_buyer=self.company)

    def test_player_source_field_is_None_by_default(self):
        self.assertIsNone(self.entry.player_source)

    def test_player_source_field_points_to_Player(self):
        LogEntry.objects.create(game=self.game, player_source=self.player)

    def test_company_source_field_is_None_by_default(self):
        self.assertIsNone(self.entry.company_source)

    def test_company_source_field_points_to_Company(self):
        LogEntry.objects.create(game=self.game, company_source=self.company)

    def test_price_field_is_0_by_default(self):
        self.assertEqual(self.entry.price, 0)

    def test_shares_field_is_0_by_default(self):
        self.assertEqual(self.entry.shares, 0)

    def test_company_field_is_None_by_default(self):
        self.assertIsNone(self.entry.company)

    def test_company_field_points_to_Company(self):
        LogEntry.objects.create(game=self.game, company=self.company)

    def test_mode_field_is_None_by_default(self):
        self.assertIsNone(self.entry.mode)

    def test_mode_field_can_be_FULL(self):
        LogEntry.objects.create(game=self.game, mode=LogEntry.FULL)

    def test_mode_field_can_be_HALF(self):
        LogEntry.objects.create(game=self.game, mode=LogEntry.HALF)

    def test_mode_field_can_be_WITHHOLD(self):
        LogEntry.objects.create(game=self.game, mode=LogEntry.WITHHOLD)

    def test_are_sorted_chronological(self):
        self.entry.delete()
        entry1 = LogEntry.objects.create(game=self.game,
            time=timezone.make_aware(datetime(1970, 1, 1, 12, 0, 0)))
        entry2 = LogEntry.objects.create(game=self.game,
            time=timezone.make_aware(datetime(1970, 1, 2, 1, 0, 0)))
        entry3 = LogEntry.objects.create(game=self.game,
            time=timezone.make_aware(datetime(1970, 1, 1, 18, 0, 0)))
        self.assertEqual(list(self.game.log.all()), [entry1, entry3, entry2])

    def test_string_representation(self):
        entry = LogEntry(game=self.game, text='Test log entry')
        self.assertIn('Test log entry', str(entry))
        self.assertIn(str(entry.time), str(entry))

    def test_is_undoable_is_false_by_default(self):
        self.assertFalse(self.entry.is_undoable)

    def test_transfer_money_is_undoable(self):
        self.entry.action = LogEntry.TRANSFER_MONEY
        self.assertTrue(self.entry.is_undoable)

    def test_transfer_share_is_undoable(self):
        self.entry.action = LogEntry.TRANSFER_SHARE
        self.assertTrue(self.entry.is_undoable)

    def test_operate_is_undoable(self):
        self.entry.action = LogEntry.OPERATE
        self.assertTrue(self.entry.is_undoable)
