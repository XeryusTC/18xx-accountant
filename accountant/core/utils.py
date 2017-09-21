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

def undo(game):
    affected = {'game': game}
    entry = game.log_cursor
    if entry.action == models.LogEntry.TRANSFER_MONEY:
        if entry.acting_player is not None:
            transfer_money(None, entry.acting_player, entry.amount)
            affected['players'] = [entry.acting_player]
        elif entry.acting_company is not None:
            transfer_money(None, entry.acting_company, entry.amount)
            affected['companies'] = [entry.acting_company]

    game.refresh_from_db()
    game.log_cursor = game.log.filter(time__lt=entry.time).last()
    game.save()
    return affected

def redo(game):
    entry = game.log.filter(time__gt=game.log_cursor.time).first()
    affected = {'game': game, 'log': entry}

    if entry.action == models.LogEntry.TRANSFER_MONEY:
        transfer_money(entry.acting_player, None, entry.amount)
        affected['players'] = [entry.acting_player]

    game.refresh_from_db()
    game.log_cursor = entry
    game.save()
    return affected
