# -*- coding: utf-8 -*-
from page_objects import PageObject, PageElement, MultiPageElement

class Homepage(PageObject):
    stylesheets = MultiPageElement(tag_name='link')
    scripts = MultiPageElement(tag_name='script')
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
    _share_count = PageElement(css=".share_count", context=True)
    _ipo_shares = PageElement(css=".ipo", context=True)
    _bank_shares = PageElement(css=".bank", context=True)
    _detail = PageElement(css=".detail", context=True)
    _summary = PageElement(css=".row", context=True)

    def get_players(self):
        res = []
        for row in self._player_list:
            info = {
                'row': row,
                'name': self._name(row),
                'cash': self._cash(row),
                'detail': self._detail(row),
            }
            res.append(info)
        return res

    def get_companies(self):
        res = []
        for row in self._company_list:
            info = {
                'elem': self._summary(row),
                'name': self._name(row),
                'cash': self._cash(row),
                'share_count': self._share_count(row),
                'ipo_shares': self._ipo_shares(row),
                'bank_shares': self._bank_shares(row),
                'detail': self._detail(row),
            }
            res.append(info)
        return res


class AddPlayerPage(PageObject):
    name = PageElement(name='name')
    cash = PageElement(name='cash')
    add_button = PageElement(tag_name='button')
    header = PageElement(id_='title')
    error_list = PageElement(css='.errorlist')
    back = PageElement(id_='back')
    game = PageElement(name='game')


class AddCompanyPage(PageObject):
    header = PageElement(id_='title')
    name = PageElement(name='name')
    cash = PageElement(name='cash')
    shares = PageElement(name='share_count')
    add_button = PageElement(tag_name='button')
    game = PageElement(name='game')
    error_list = PageElement(css='.errorlist')
    back = PageElement(id_='back')
    text_color = MultiPageElement(name='text-color-select')
    background_color = MultiPageElement(name='background-color-select')
