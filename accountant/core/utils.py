# -*- coding: utf-8 -*-

def transfer_money(sender, receiver, amount):
    if sender is None:
        sender = receiver.game
    if receiver is None:
        receiver = sender.game
    sender.cash -= amount
    receiver.cash += amount
