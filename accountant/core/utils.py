# -*- coding: utf-8 -*-
from enum import Enum
import math
from . import models

class SameEntityError(Exception):
    pass


class InvalidShareTransaction(Exception):
    pass


class DifferentGameException(InvalidShareTransaction):
    pass


class Share(Enum):
    IPO = 1
    BANK = 2


class OperateMethod(Enum):
    FULL = 1
    WITHHOLD = 2
    HALF = 3


def transfer_money(sender, receiver, amount):
    if sender == receiver:
        raise SameEntityError()
    if sender is None:
        sender = receiver.game
    if receiver is None:
        receiver = sender.game
    sender.cash -= amount
    receiver.cash += amount
    sender.save()
    receiver.save()

def buy_share(buyer, company, source, price, amount=1):
    # Check if shares are available
    if source == Share.IPO and company.ipo_shares < amount:
        raise InvalidShareTransaction()
    elif source == Share.BANK and company.bank_shares < amount:
        raise InvalidShareTransaction()

    if isinstance(source, models.Company):  # Share comes from a company
        try:
            source_share = models.CompanyShare.objects.get(owner=source,
                company=company)
        except models.CompanyShare.DoesNotExist:
            if amount < 0:
                source_share = models.CompanyShare.objects.create(
                    owner=source, company=company, shares=0)
            else:
                raise InvalidShareTransaction()
        if source_share.shares < amount:
            raise InvalidShareTransaction()
    elif isinstance(source, models.Player):  # Share comes from a player
        try:
            source_share = models.PlayerShare.objects.get(owner=source,
                company=company)
        except models.PlayerShare.DoesNotExist:
            source_share = models.PlayerShare.objects.create(owner=source,
                company=company, shares=0)
    else:
        source_share = None

    # Check if the buyer, company and source are in the same game
    if source not in Share and source.game != company.game:
        raise DifferentGameException()
    if buyer not in Share and buyer.game != company.game:
        raise DifferentGameException()

    # Buy the shares
    if buyer == Share.IPO:
        company.ipo_shares += amount
        company.save()
    elif buyer == Share.BANK:
        company.bank_shares += amount
        company.save()
    else:  # Comes from company or player
        # Create share object if necessary
        try:
            share = buyer.share_set.get(company=company)
        except models.PlayerShare.DoesNotExist:
            share = models.PlayerShare.objects.create(owner=buyer,
                company=company, shares=0)
        except models.CompanyShare.DoesNotExist:
            share = models.CompanyShare.objects.create(owner=buyer,
                company=company, shares=0)
        share.shares += amount
        share.save()

    # Remove the share from the source
    if source_share:
        source_share.shares -= amount
        source_share.save()
    elif source == Share.IPO:
        company.ipo_shares -= amount
        company.save()
    elif source == Share.BANK:
        company.bank_shares -= amount
        company.save()

    # Update buyer instance if company is buying in itself
    if isinstance(buyer, models.Company) and company.pk == buyer.pk:
        buyer.refresh_from_db()
    # Update source instance if company is selling itself
    if isinstance(source, models.Company) and company.pk == source.pk:
        source.refresh_from_db()

    # Transfer the money
    if buyer in (Share.BANK, Share.IPO):
        buyer = None
    if source in (Share.BANK, Share.IPO):
        transfer_money(buyer, None, price * amount)
    else:
        transfer_money(buyer, source, price * amount)

    # Refresh company to get changes is cash
    company.refresh_from_db()

def operate(company, amount, method):
    affected = {}
    if method == OperateMethod.WITHHOLD:
        affected[company] = amount
    elif method == OperateMethod.HALF:
        withhold = amount / 2
        distribute = amount / 2
        affected = _distribute_dividends(company, distribute)
        # If not every entity receives an integer amount then we have to
        # round in favour of the share holders
        if not all(d.is_integer() for e, d in affected.items()):
            distribute = math.ceil(distribute / company.share_count)
            distribute *= company.share_count
            withhold = amount - distribute
            affected = _distribute_dividends(company, distribute)
        if company not in affected:
            affected[company] = 0
        affected[company] += withhold
    elif method == OperateMethod.FULL:
        affected = _distribute_dividends(company, amount)
        # If some entities don't receive an integer amount then we have to
        # get rid of the remainder
        if not all(d.is_integer() for e, d in affected.items()):
            for entity in affected:
                affected[entity] = math.floor(affected[entity])

    # Pay actual dividends
    for entity, amount in affected.items():
        transfer_money(None, entity, amount)
    return affected

def _distribute_dividends(company, amount):
    result = {}
    dividends_per_share = amount / company.share_count
    # Calculate dividends paid to players
    for share in company.playershare_set.all():
        dividend = dividends_per_share * share.shares
        if dividend != 0:
            result[share.owner] = dividend
    # Calculate dividends paid to companies
    if company.game.treasury_shares_pay:
        for share in company.companyshare_set.all():
            dividend = dividends_per_share  * share.shares
            if dividend != 0:
                result[share.owner] = dividend
    # Calculate dividends paid by pool shares to the owning company
    if company.game.pool_shares_pay and company.bank_shares != 0:
        dividend = dividends_per_share * company.bank_shares
        if dividend != 0:
            try:
                result[company] += dividend
            except KeyError:
                result[company] = dividend
    # Calculate dividends paid by IPO shares to the company
    if company.game.ipo_shares_pay and company.ipo_shares != 0:
        dividend = dividends_per_share * company.ipo_shares
        if dividend != 0:
            try:
                result[company] += dividend
            except KeyError:
                result[company] = dividend
    return result

def create_log_entry(game, action, **kwargs):
    # Delete all entries that are on the redo stack
    if game.log_cursor:
        game.log.filter(time__gt=game.log_cursor.time).delete()

    # Create new entry
    entry = models.LogEntry.objects.create(game=game, action=action)
    if action == models.LogEntry.TRANSFER_MONEY:
        entry.amount = kwargs['amount']
        if isinstance(kwargs['acting'], models.Player):
            entry.acting_player = kwargs['acting']
        elif isinstance(kwargs['acting'], models.Company):
            entry.acting_company = kwargs['acting']
        if 'receiving' in kwargs.keys():
            if isinstance(kwargs['receiving'], models.Player):
                entry.receiving_player = kwargs['receiving']
            elif isinstance(kwargs['receiving'], models.Company):
                entry.receiving_company = kwargs['receiving']
    elif action == models.LogEntry.TRANSFER_SHARE:
        entry.shares = kwargs['shares']
        entry.price = kwargs['price']
        entry.company = kwargs['company']
        if isinstance(kwargs['buyer'], models.Player):
            entry.buyer = 'player'
            entry.player_buyer = kwargs['buyer']
        elif isinstance(kwargs['buyer'], models.Company):
            entry.buyer = 'company'
            entry.company_buyer = kwargs['buyer']
            entry.acting_company = kwargs['buyer']
        if kwargs['source'] == Share.IPO:
            entry.source = 'ipo'
        elif kwargs['source'] == Share.BANK:
            entry.source = 'bank'
        elif isinstance(kwargs['source'], models.Player):
            entry.source = 'player'
            entry.player_source = kwargs['source']
        elif isinstance(kwargs['source'], models.Company):
            entry.source = 'company'
            entry.company_source = kwargs['source']
    elif action == models.LogEntry.OPERATE:
        entry.amount = kwargs['amount']
        entry.acting_company = kwargs['company']
        entry.mode = kwargs['mode']
    if 'text' in kwargs.keys():
        entry.text = kwargs['text']
    if 'acting_company' in kwargs.keys():
        entry.acting_company = kwargs['acting_company']
    entry.save()
    game.log_cursor = entry
    game.save()
    return entry

def undo(game):
    entry = game.log_cursor
    f, kwargs, affected = _action_call(entry)
    kwargs['amount'] *= -1
    f(**kwargs)

    if 'game' in affected:
        affected['game'].refresh_from_db()
    for name in ('companies', 'players', 'shares'):
        if name in affected:
            for i, inst in enumerate(affected[name]):
                inst.refresh_from_db()
                affected[name][i] = inst

    game.refresh_from_db()
    game.log_cursor = game.log.filter(time__lt=entry.time).last()
    game.save()
    return affected

def redo(game):
    entry = game.log.filter(time__gt=game.log_cursor.time).first()
    f, kwargs, affected = _action_call(entry)
    f(**kwargs)

    for name in ('companies', 'players', 'shares'):
        if name in affected:
            for i, inst in enumerate(affected[name]):
                inst.refresh_from_db()
                affected[name][i] = inst

    game.refresh_from_db()
    game.log_cursor = entry
    game.save()
    affected['log'] = entry
    return affected

def _action_call(entry):
    affected = {'players': [], 'companies': []}
    kwargs = {}
    if entry.action == models.LogEntry.TRANSFER_MONEY:
        f = transfer_money
        kwargs = {'sender': None, 'receiver': None, 'amount': entry.amount}
        # Determine who originally send money
        if entry.acting_player is not None:
            kwargs['sender'] = entry.acting_player
            affected['players'].append(entry.acting_player)
        elif entry.acting_company is not None:
            kwargs['sender'] = entry.acting_company
            affected['companies'].append(entry.acting_company)
        else:
            affected['game'] = entry.game
        # Determine who originally received money
        if entry.receiving_player is not None:
            kwargs['receiver'] = entry.receiving_player
            affected['players'].append(entry.receiving_player)
        elif entry.receiving_company is not None:
            kwargs['receiver'] = entry.receiving_company
            affected['companies'].append(entry.receiving_company)
        else:
            affected['game'] = entry.game
    elif entry.action == models.LogEntry.TRANSFER_SHARE:
        f = buy_share
        kwargs = {'price': entry.price, 'amount': entry.shares,
            'company': entry.company}
        affected['shares'] = []
        # Determine who bought the share
        if entry.buyer == 'player':
            kwargs['buyer'] = entry.player_buyer
            affected['players'].append(entry.player_buyer)
            affected['shares'].append(entry.player_buyer.share_set.get(
                company=entry.company))
        elif entry.buyer == 'company':
            kwargs['buyer'] = entry.company_buyer
            affected['companies'].append(entry.company_buyer)
            affected['shares'].append(entry.company_buyer.share_set.get(
                company=entry.company))
        # Determine where the share came from
        if entry.source == 'ipo':
            kwargs['source'] = Share.IPO
            affected['game'] = entry.game
            affected['companies'].append(entry.company)
        elif entry.source == 'bank':
            kwargs['source'] = Share.BANK
            affected['game'] = entry.game
            affected['companies'].append(entry.company)
        elif entry.source == 'player':
            kwargs['source'] = entry.player_source
            affected['players'].append(entry.player_source)
            affected['shares'].append(entry.player_source.share_set.get(
                company=entry.company))
        elif entry.source == 'company':
            kwargs['source'] = entry.company_source
            affected['companies'].append(entry.company_source)
            affected['shares'].append(entry.company_source.share_set.get(
                company=entry.company))
    elif entry.action == models.LogEntry.OPERATE:
        f = operate
        affected['game'] = entry.game
        affected['players'] = list(entry.acting_company.player_owners.all())
        affected['companies'] = list(entry.acting_company.company_owners.all())
        kwargs['company'] = entry.acting_company
        kwargs['amount'] = entry.amount
        if entry.mode == models.LogEntry.FULL:
            kwargs['method'] = OperateMethod.FULL
        elif entry.mode == models.LogEntry.HALF:
            kwargs['method'] = OperateMethod.HALF
            affected['companies'].append(entry.acting_company)
        else:
            kwargs['method'] = OperateMethod.WITHHOLD
            affected['players'] = []
            affected['companies'] = [entry.acting_company]

    # Remove empty items from affected
    if not affected['players']:
        del affected['players']
    if not affected['companies']:
        del affected['companies']
    return f, kwargs, affected
