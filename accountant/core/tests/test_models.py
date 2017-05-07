# -*- coding: utf-8 -*-
from django.db.utils import IntegrityError
from django.test import TestCase
import uuid

from .. import factories
from ..models import Game, Player, Company, PlayerShare, CompanyShare

class GameTests(TestCase):
    def test_pk_is_uuid(self):
        game = Game()
        game.save()
        self.assertIsInstance(game.pk, uuid.UUID)

    def test_bank_cash_is_12000_by_default(self):
        game = Game()
        self.assertEqual(game.cash, 12000)

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
        p1 = factories.PlayerFactory.create(name='Alice', game=self.game)
        p2 = Player(name='Alice', game=self.game)
        with self.assertRaises(IntegrityError):
            p2.save()

    def test_can_create_players_with_different_name_in_the_same_game(self):
        p1 = factories.PlayerFactory.create(name='Alice', game=self.game)
        p2 = Player(name='Bob', game=self.game)
        p2.save()

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
        c1 = factories.CompanyFactory.create(name='B&O', game=self.game)
        c2 = Company(name='B&O', game=self.game)
        with self.assertRaises(IntegrityError):
            c2.save()

    def test_can_create_companies_with_different_name_in_the_same_game(self):
        c1 = factories.CompanyFactory.create(name='B&O', game=self.game)
        c2 = Company(name='C&O', game=self.game)
        c2.save()

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
        company = Company(text_color='blue-500')

    def test_default_text_color_is_black(self):
        company = Company(game=self.game)
        self.assertEqual(company.text_color, 'black')

    def test_has_background_color(self):
        company = Company(background_color='white')

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
        share = PlayerShare.objects.create(owner=self.player,
            company=self.company)
        self.assertIn(self.company, list(self.player.shares.all()))

    def test_player_owns_one_share_by_default(self):
        player = factories.PlayerFactory.create(game=self.game)
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
        share = CompanyShare.objects.create(owner=self.company1,
            company=self.company2)
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
