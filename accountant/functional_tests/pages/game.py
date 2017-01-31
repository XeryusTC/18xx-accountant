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
