# -*- coding: utf-8 -*-
from django import forms

class CreateGameForm(forms.Form):
    bank_cash = forms.IntegerField(required=False, initial=12000)

    def clean_bank_cash(self):
        data = self.cleaned_data['bank_cash']
        if data == None:
            data = 0
        return data


class AddPlayerForm(forms.Form):
    name = forms.CharField()
    cash = forms.CharField()
