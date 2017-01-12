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
    if source == IPO_SHARES and company.ipo_shares == 0:
        raise InvalidShareTransaction()
    elif source == BANK_SHARES and company.bank_shares == 0:
        raise InvalidShareTransaction()

    if isinstance(source, models.Company): # Share comes from a company
        try:
            source_share = source.companyshare_set.get(company=source)
        except models.CompanyShare.DoesNotExist:
            raise InvalidShareTransaction()
        if source_share.shares < amount:
            raise InvalidShareTransaction()
    else:
        source_share = None

    # Create share object if necessary
    try:
        share = buyer.share_set.get(company=company)
    except models.PlayerShare.DoesNotExist:
        share = models.PlayerShare.objects.create(owner=buyer,
            company=company, shares=0)
    except models.CompanyShare.DoesNotExist:
        share = models.CompanyShare.objects.create(owner=buyer,
            company=company, shares=0)

    # Buy the share
    share.shares += amount
    share.save()

    # Remove the share from the source
    if source_share:
        source_share.shares -= amount
        source_share.save()

    # Transfer the money
    if source in (BANK_SHARES, IPO_SHARES):
        transfer_money(buyer, None, price)
    else:
        transfer_money(buyer, source, price)
