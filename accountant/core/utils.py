# -*- coding: utf-8 -*-
from . import models

IPO_SHARES  = 1
BANK_SHARES = 2

class SameEntityError(Exception):
    pass


class InvalidShareTransaction(Exception):
    pass


def transfer_money(sender, receiver, amount):
    if sender == receiver:
        raise SameEntityError()
    if sender is None:
        sender = receiver.game
    if receiver is None:
        receiver = sender.game
    sender.cash -= amount
    receiver.cash += amount

def buy_share(buyer, company, source, price, amount=1):
    # Check if shares are available
    if source == IPO_SHARES and company.ipo_shares < amount:
        raise InvalidShareTransaction()
    elif source == BANK_SHARES and company.bank_shares < amount:
        raise InvalidShareTransaction()

    if isinstance(source, models.Company): # Share comes from a company
        try:
            source_share = models.CompanyShare.objects.get(owner=source,
                company=company)
        except models.CompanyShare.DoesNotExist:
            raise InvalidShareTransaction()
        if source_share.shares < amount:
            raise InvalidShareTransaction()
    elif isinstance(source, models.Player): # Share comes from a player
        try:
            source_share = models.PlayerShare.objects.get(owner=source,
                company=company)
        except models.PlayerShare.DoesNotExist:
            source_share = models.PlayerShare.objects.create(owner=source,
                company=company, shares=0)
    else:
        source_share = None

    # Buy the shares
    if buyer == IPO_SHARES:
        company.ipo_shares += amount
        company.save()
    elif buyer == BANK_SHARES:
        company.bank_shares += amount
        company.save()
    else: # Comes from company or player
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
    elif source == IPO_SHARES:
        company.ipo_shares -= amount
        company.save()
    elif source == BANK_SHARES:
        company.bank_shares -= amount
        company.save()

    # Transfer the money
    if buyer in (BANK_SHARES, IPO_SHARES):
        buyer = None
    if source in (BANK_SHARES, IPO_SHARES):
        transfer_money(buyer, None, price * amount)
    else:
        transfer_money(buyer, source, price * amount)
