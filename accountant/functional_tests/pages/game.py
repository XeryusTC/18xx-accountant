# -*- coding: utf-8 -*-
from page_objects import PageObject, PageElement, MultiPageElement

class Homepage(PageObject):
    stylesheets = MultiPageElement(tag_name='link')
    scripts = MultiPageElement(tag_name='script')
    start_button = PageElement(name='new_game')
    bank_cash = PageElement(name='cash')
    app_root = PageElement(tag_name='app-root')
    pool_shares_pay = PageElement(name='pool-shares-pay')
    ipo_shares_pay = PageElement(name='ipo-shares-pay')

class GamePage(PageObject):
    add_player_link = PageElement(id_='add_player')
    add_company_link = PageElement(id_='add_company')
    bank_cash = PageElement(css="#bank #cash")
    bank_pool = MultiPageElement(css="#bank .pool")
    pool_shares_pay = PageElement(name='pool-shares-pay')
    ipo_shares_pay = PageElement(name='ipo-shares-pay')

    player_name_list = MultiPageElement(css="div.player div.name")

    log = MultiPageElement(css="#log div.entry")

    _player_list = MultiPageElement(class_name="player")
    _company_list = MultiPageElement(class_name="company")

    def get_players(self):
        res = []
        for row in self._player_list:
            res.append(Player(row, self.w))
        return res

    def get_companies(self):
        res = []
        for row in self._company_list:
            res.append(Company(row, self.w))
        return res


class Entity(PageObject):
    _name = PageElement(css=".name", context=True)
    _cash = PageElement(css=".cash", context=True)
    _detail = PageElement(css=".detail", context=True)
    _shares = MultiPageElement(css=".share", context=True)
    _summary = PageElement(css=".row", context=True)

    def __init__(self, root, *args, **kwargs):
        super(Entity, self).__init__(*args, **kwargs)
        self.root = root

    def __getitem__(self, key):
        if key == 'row':
            return self.root
        elif key == 'elem' or key == 'summary':
            return self._summary(self.root)
        elif key == 'name':
            return self._name(self.root)
        elif key == 'cash':
            return self._cash(self.root)
        elif key == 'shares':
            return self._shares(self.root)
        elif key == 'detail':
            return self._detail(self.root)
        else:  # pragma: no cover
            raise KeyError


class Player(Entity):
    pass


class Company(Entity):
    _value = PageElement(css=".value input", context=True)
    _share_count = PageElement(css=".share_count", context=True)
    _ipo_shares = PageElement(css=".ipo", context=True)
    _bank_shares = PageElement(css=".bank", context=True)

    def __getitem__(self, key):
        if key == 'share_count':
            return self._share_count(self.root)
        elif key == 'ipo_shares':
            return self._ipo_shares(self.root)
        elif key == 'bank_shares':
            return self._bank_shares(self.root)
        elif key == 'value':
            return self._value(self.root)
        return super(Company, self).__getitem__(key)


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
    preview = PageElement(id_='preview')

    def select_text_color(self, color):
        for radio in self.text_color:
            if radio.get_attribute('value') == color:
                radio.click()
                break

    def select_background_color(self, color):
        for radio in self.background_color:
            if radio.get_attribute('value') == color:
                radio.click()
                break


class TransferForm(PageObject):
    amount = PageElement(name='amount', context=True)
    target = MultiPageElement(name='target', context=True)
    labels = MultiPageElement(css='label.transfer', context=True)
    transfer_button = PageElement(name='transfer', context=True)

    def select_target(self, name, context):  # pragma: no cover
        for radio in self.target(context):
            if radio.get_attribute('id') == 'target-{}'.format(name):
                radio.click()
                break
        else:
            self.fail('Could not find {} in the transfer form'.format(name))


class ShareForm(PageObject):
    shares = PageElement(name='shares', context=True)
    company = MultiPageElement(css='label.company-label', context=True)
    source = MultiPageElement(css='label.source', context=True)
    transfer_button = PageElement(name='transfer-share', context=True)
    buy_share = PageElement(id_='action-buy', context=True)
    sell_share = PageElement(id_='action-sell', context=True)
    action = PageElement(id_='action-text', context=True)

    def select_company(self, name, context):  # pragma: no cover
        for label in self.company(context):
            if label.get_attribute('for') == 'company-{}'.format(name):
                label.click()
                break
        else:  # pragma: no cover
            raise AssertionError(
                'No company called {} found in share list'.format(name))

    def select_source(self, name, context):  # pragma: no cover
        for label in self.source(context):
            if label.get_attribute('for') == 'source-{}'.format(name):
                label.click()
                break
        else:
            raise AssertionError('Could not select {}'.format(name))


class OperateForm(PageObject):
    revenue  = PageElement(name='revenue',  context=True)
    full     = PageElement(name='full',     context=True)
    half     = PageElement(name='half',     context=True)
    withhold = PageElement(name='withhold', context=True)


class ErrorPage(PageObject):
    errors = MultiPageElement(css=".error")
    close = PageElement(css='.close')
