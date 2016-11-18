# -*- coding: utf-8 -*-
from page_objects import PageObject, MultiPageElement

class Homepage(PageObject):
    stylesheets = MultiPageElement(tag_name='link')
