# -*- coding: utf-8 -*-
from django.core.management import call_command, CommandError
from django.test import TestCase
from django.utils.six import StringIO

from .. import factories
from .. import models

FAKE_UUID = '00000000-0000-0000-0000-000000000000'

class CreategameTests(TestCase):
    def test_creates_game(self):
        self.assertEqual(models.Game.objects.count(), 0)
        call_command('creategame')
        self.assertEqual(models.Game.objects.count(), 1)

    def test_outputs_uuid_of_new_game(self):
        out = StringIO()
        call_command('creategame', stdout=out)
        self.assertEqual(out.getvalue().strip(),
            str(models.Game.objects.first().pk))

    def test_cash_parameter_determines_bank_size(self):
        call_command('creategame', cash=100)
        self.assertEqual(models.Game.objects.first().cash, 100)

    def test_without_cash_parameter_creates_bank_of_12000(self):
        call_command('creategame')
        self.assertEqual(models.Game.objects.first().cash, 12000)


class CreateplayerTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory.create()

    def test_requires_game_uuid(self):
        with self.assertRaises(CommandError) as cm:
            call_command('createplayer')
        self.assertIn('game', cm.exception.args[0])

    def test_requires_name(self):
        with self.assertRaises(CommandError) as cm:
            call_command('createplayer')
        self.assertIn('name', cm.exception.args[0])

    def test_creates_player(self):
        self.assertEqual(models.Player.objects.count(), 0)
        call_command('createplayer', str(self.game.pk), 'Alice')
        self.assertEqual(models.Player.objects.count(), 1)

    def test_outputs_uuid_of_new_player(self):
        out = StringIO()
        call_command('createplayer', str(self.game.pk), 'Bob', stdout=out)
        self.assertEqual(out.getvalue().strip(),
            str(models.Player.objects.first().pk))

    def test_player_game_is_same_as_game_parameter(self):
        call_command('createplayer', str(self.game.pk), 'Fred')
        self.assertEqual(models.Player.objects.first().game, self.game)

    def test_player_name_is_same_as_name_parameter(self):
        call_command('createplayer', str(self.game.pk), 'George')
        self.assertEqual(models.Player.objects.first().name, 'George')

    def test_raises_CommandError_when_game_doesnt_exist(self):
        with self.assertRaises(CommandError) as cm:
            call_command('createplayer', 'fake-uuid', 'Charlie')
        self.assertIn('This is not a valid UUID', cm.exception.args)

    def test_cash_parameter_determines_amount_of_cash_player_has(self):
        call_command('createplayer', str(self.game.pk), 'Dave', cash=1000)
        self.assertEqual(models.Player.objects.first().cash, 1000)

    def test_without_cash_parameter_player_has_no_cash(self):
        call_command('createplayer', str(self.game.pk), 'Eve')
        self.assertEqual(models.Player.objects.first().cash, 0)


class CreatecompanyTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory.create()

    def test_requires_game_uuid(self):
        with self.assertRaises(CommandError) as cm:
            call_command('createcompany')
        self.assertIn('game', cm.exception.args[0])

    def test_requires_name(self):
        with self.assertRaises(CommandError) as cm:
            call_command('createcompany')
        self.assertIn('name', cm.exception.args[0])

    def test_creates_company(self):
        self.assertEqual(models.Company.objects.count(), 0)
        call_command('createcompany', str(self.game.pk), 'B&O')
        self.assertEqual(models.Company.objects.count(), 1)

    def test_outputs_uuid_of_new_company(self):
        out = StringIO()
        call_command('createcompany', str(self.game.pk), 'B&M', stdout=out)
        self.assertEqual(out.getvalue().strip(),
            str(models.Company.objects.first().pk))

    def test_company_game_is_same_as_game_parameter(self):
        call_command('createcompany', str(self.game.pk), 'CPR')
        self.assertEqual(models.Company.objects.first().game, self.game)

    def test_company_name_is_same_as_name_parameter(self):
        call_command('createcompany', str(self.game.pk), 'C&O')
        self.assertEqual(models.Company.objects.first().name, 'C&O')

    def test_raises_CommandError_when_game_doesnt_exist(self):
        with self.assertRaises(CommandError) as cm:
            call_command('createcompany', 'fake-uuid', 'Erie')
        self.assertIn('This is not a valid UUID', cm.exception.args)

    def test_cash_parameter_determines_amount_of_cash_company_has(self):
        call_command('createcompany', str(self.game.pk), 'NYC', cash=97)
        self.assertEqual(models.Company.objects.first().cash, 97)

    def test_without_cash_parameter_company_has_no_cash(self):
        call_command('createcompany', str(self.game.pk), 'N&W')
        self.assertEqual(models.Company.objects.first().cash, 0)

    def test_share_count_parameter_determines_company_share_count(self):
        call_command('createcompany', str(self.game.pk), 'NKP', share_count=7)
        self.assertEqual(models.Company.objects.first().share_count, 7)

    def test_without_share_count_parameter_company_has_10_shares(self):
        call_command('createcompany', str(self.game.pk), 'B&M')
        self.assertEqual(models.Company.objects.first().share_count, 10)

    def test_ipo_param_determines_company_ipo_shares(self):
        call_command('createcompany', str(self.game.pk), 'RDR', ipo_shares=5)
        self.assertEqual(models.Company.objects.first().ipo_shares, 5)

    def test_without_ipo_param_company_has_10_ipo_shares(self):
        call_command('createcompany', str(self.game.pk), 'PMQ')
        self.assertEqual(models.Company.objects.first().ipo_shares, 10)

    def test_bank_param_determines_company_bank_shares(self):
        call_command('createcompany', str(self.game.pk), 'NNH', bank=3)
        self.assertEqual(models.Company.objects.first().bank_shares, 3)

    def test_withoubank_param_determines_company_has_0_bank_shares(self):
        call_command('createcompany', str(self.game.pk), 'NNH')
        self.assertEqual(models.Company.objects.first().bank_shares, 0)

    def test_text_color_param_sets_company_text_color(self):
        call_command('createcompany', str(self.game.pk), 'PRR',
            text_color='red-700')
        self.assertEqual(models.Company.objects.first().text_color, 'red-700')

    def test_text_color_param_is_black_by_default(self):
        call_command('createcompany', str(self.game.pk), 'C&O')
        self.assertEqual(models.Company.objects.first().text_color, 'black')

    def test_background_color_param_sets_company_background_color(self):
        call_command('createcompany', str(self.game.pk), 'Erie',
            background_color='yellow-600')
        self.assertEqual(models.Company.objects.first().background_color,
            'yellow-600')

    def test_background_color_param_is_white_by_default(self):
        call_command('createcompany', str(self.game.pk), 'B&O')
        self.assertEqual(models.Company.objects.first().background_color,
            'white')

class CreateplayershareTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory.create()
        self.player = factories.PlayerFactory.create(game=self.game)
        self.company = factories.CompanyFactory.create(game=self.game)

    def test_requires_player_uuid(self):
        with self.assertRaises(CommandError) as cm:
            call_command('createplayershare')
        self.assertIn('owner', cm.exception.args[0])

    def test_requires_company_uuid(self):
        with self.assertRaises(CommandError) as cm:
            call_command('createplayershare')
        self.assertIn('company', cm.exception.args[0])

    def test_outputs_uuid_of_new_share(self):
        out = StringIO()
        call_command('createplayershare', str(self.player.pk),
            str(self.company.pk), stdout=out)
        self.assertEqual(out.getvalue().strip(),
            str(models.PlayerShare.objects.first().pk))

    def test_shares_owned_is_same_as_shares_parameter(self):
        call_command('createplayershare', str(self.player.pk),
            str(self.company.pk), shares=3)
        self.assertEqual(models.PlayerShare.objects.first().shares, 3)

    def test_shares_owned_is_one_by_default(self):
        call_command('createplayershare', str(self.player.pk),
            str(self.company.pk))
        self.assertEqual(models.PlayerShare.objects.first().shares, 1)

    def test_raises_CommandError_when_player_doesnt_exist(self):
        with self.assertRaises(CommandError) as cm:
            call_command('createplayershare', FAKE_UUID, str(self.company.pk))
        self.assertIn('This is not a valid UUID', cm.exception.args)

    def test_raises_CommandError_when_company_doesnt_exist(self):
        with self.assertRaises(CommandError) as cm:
            call_command('createplayershare', str(self.player.pk), FAKE_UUID)
        self.assertIn('This is not a valid UUID', cm.exception.args)

    def test_CommandError_when_player_and_company_not_in_the_same_game(self):
        player = factories.PlayerFactory.create()
        company = factories.CompanyFactory.create()
        with self.assertRaises(CommandError) as cm:
            call_command('createplayershare', str(player.pk), str(company.pk))
        self.assertIn('Owner and company are not in the same game',
            cm.exception.args)

    def test_updates_existing_record_with_new_share_amount(self):
        factories.PlayerShareFactory.create(owner=self.player,
            company=self.company, shares=1)
        call_command('createplayershare', str(self.player.pk),
            str(self.company.pk), shares=4)
        self.assertEqual(models.PlayerShare.objects.first().shares, 4)

    def test_updating_shares_outputs_share_uuid(self):
        out = StringIO()
        share = factories.PlayerShareFactory.create(owner=self.player,
            company=self.company, shares=2)
        call_command('createplayershare', str(self.player.pk),
            str(self.company.pk), shares=5, stdout=out)
        self.assertEqual(out.getvalue().strip(), str(share.pk))


class CreatecompanyshareTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory.create()
        self.owner = factories.CompanyFactory.create(game=self.game)
        self.company = factories.CompanyFactory.create(game=self.game)

    def test_requires_owner_uuid(self):
        with self.assertRaises(CommandError) as cm:
            call_command('createcompanyshare')
        self.assertIn('owner', cm.exception.args[0])

    def test_requires_company_uuid(self):
        with self.assertRaises(CommandError) as cm:
            call_command('createcompanyshare')
        self.assertIn('company', cm.exception.args[0])

    def test_shares_owned_is_same_as_shares_parameter(self):
        call_command('createcompanyshare', str(self.owner.pk),
            str(self.company.pk), shares=7)
        self.assertEqual(models.CompanyShare.objects.first().shares, 7)

    def test_shares_owned_is_one_by_default(self):
        call_command('createcompanyshare', str(self.owner.pk),
            str(self.company.pk))
        self.assertEqual(models.CompanyShare.objects.first().shares, 1)

    def test_updates_existing_record_with_new_share_amount(self):
        factories.CompanyShareFactory.create(owner=self.owner,
            company=self.company, shares=2)
        call_command('createcompanyshare', str(self.owner.pk),
            str(self.company.pk), shares=5)
        self.assertEqual(models.CompanyShare.objects.first().shares, 5)
        self.assertEqual(models.CompanyShare.objects.count(), 1)

    def test_outputs_uuid_of_new_share(self):
        out = StringIO()
        call_command('createcompanyshare', str(self.owner.pk),
            str(self.company.pk), stdout=out)
        self.assertEqual(out.getvalue().strip(),
            str(models.CompanyShare.objects.first().pk))

    def test_updating_shares_outputs_share_uuid(self):
        out = StringIO()
        share = factories.CompanyShareFactory.create(owner=self.owner,
            company=self.company, shares=3)
        call_command('createcompanyshare', str(self.owner.pk),
            str(self.company.pk), shares=8, stdout=out)
        self.assertEqual(out.getvalue().strip(), str(share.pk))

    def test_raises_CommandError_when_owner_doesnt_exist(self):
        with self.assertRaises(CommandError) as cm:
            call_command('createcompanyshare', FAKE_UUID, str(self.owner.pk))
        self.assertIn('This is not a valid UUID', cm.exception.args)

    def test_raises_CommandError_when_company_doesnt_exist(self):
        with self.assertRaises(CommandError) as cm:
            call_command('createcompanyshare', FAKE_UUID, str(self.company.pk))
        self.assertIn('This is not a valid UUID', cm.exception.args)

    def test_CommandError_when_owner_and_company_not_in_the_same_game(self):
        owner = factories.CompanyFactory.create()
        company = factories.CompanyFactory.create()
        with self.assertRaises(CommandError) as cm:
            call_command('createcompanyshare', str(owner.pk), str(company.pk))
        self.assertIn('Owner and company are not in the same game',
            cm.exception.args)
