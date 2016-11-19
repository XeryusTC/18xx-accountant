# -*- coding: utf-8 -*-
from page_objects import PageObject, PageElement, MultiPageElement

class Homepage(PageObject):
    stylesheets = MultiPageElement(tag_name='link')
    start_button = PageElement(name='new_game')


class Housekeeping(PageObject):
    game_name = PageElement(name='game_name')
