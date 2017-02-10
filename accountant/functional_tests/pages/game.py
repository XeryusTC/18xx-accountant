# -*- coding: utf-8 -*-
from page_objects import PageObject, PageElement, MultiPageElement

class Homepage(PageObject):
    stylesheets = MultiPageElement(tag_name='link')
    start_button = PageElement(name='new_game')
    bank_cash = PageElement(name='bank_cash')

class GamePage(PageObject):
    add_player_link = PageElement(name='add_player')
    add_company_link = PageElement(name='add_company')
    bank_cash = PageElement(css="#bank #cash")

    player_name_list = MultiPageElement(css="div.player div.name")

    _player_list = MultiPageElement(class_name="player")
    _company_list = MultiPageElement(class_name="company")
    _name = PageElement(css=".name", context=True)
    _cash = PageElement(css=".cash", context=True)
    _ipo_shares = PageElement(css=".ipo", context=True)

    def get_players(self):
        res = []
        for row in self._player_list:
            info = {
                'name': self._name(row),
                'cash': self._cash(row),
            }
            res.append(info)
        return res

    def get_companies(self):
        res = []
        for row in self._company_list:
            info = {
                'name': self._name(row),
                'cash': self._cash(row),
                'ipo_shares': self._ipo_shares(row),
            }
            res.append(info)
        return res


class AddPlayerPage(PageObject):
    name = PageElement(name='name')
    cash = PageElement(name='cash')
    add_button = PageElement(tag_name='button')
    header = PageElement(name='title')
    error_list = PageElement(css='.errorlist')
    back = PageElement(id_='back')


class AddCompanyPage(PageObject):
    header = PageElement(name='title')
    name = PageElement(name='name')
    cash = PageElement(name='cash')
    shares = PageElement(name='share_count')
    add_button = PageElement(tag_name='button')
