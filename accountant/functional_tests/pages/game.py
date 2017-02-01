# -*- coding: utf-8 -*-
from page_objects import PageObject, PageElement, MultiPageElement

class Homepage(PageObject):
    stylesheets = MultiPageElement(tag_name='link')
    start_button = PageElement(name='new_game')
    bank_cash = PageElement(name='bank_cash')


class BankDetailSection(PageObject):
    cash = PageElement(css="#bank #cash")


class MenuSection(PageObject):
    add_player = PageElement(name='add_player')


class AddPlayerPage(PageObject):
    name = PageElement(name='name')
    cash = PageElement(name='cash')
    add_button = PageElement(tag_name='button')
    header = PageElement(name='title')


class PlayerSection(PageObject):
    name_list = MultiPageElement(css="div.player div.name")

    _player_list = MultiPageElement(css="#players")
    _name = PageElement(css=".name", context=True)
    _cash = PageElement(css=".cash", context=True)

    def get_players(self):
        res = []
        for row in self._player_list:
            info = {
                'name': self._name(row),
                'cash': self._cash(row),
            }
            res.append(info)
        return res
