# -*- coding: utf-8 -*-

IPO_SHARES  = 1
BANK_SHARES = 2

class SameEntityError(Exception):
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

def buy_share(buyer, company, source, amount, price):
    pass
