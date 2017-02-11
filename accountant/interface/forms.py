# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.translation import ugettext_lazy as _

from core import models

DUPLICATE_PLAYER_ERROR = \
    _('There is already a player with this name in your game')
DUPLICATE_COMPANY_ERROR = \
    _('There is already a company with this name in your game')

class CreateGameForm(forms.Form):
    bank_cash = forms.IntegerField(required=False, initial=12000)

    def clean_bank_cash(self):
        data = self.cleaned_data['bank_cash']
        if data == None:
            data = 0
        return data


class AddPlayerForm(forms.ModelForm):
    class Meta:
        model = models.Player
        fields = ('game', 'name', 'cash')

        error_messages = {
            NON_FIELD_ERRORS: {'unique_together': DUPLICATE_PLAYER_ERROR},
        }
        widgets = {
            'game': forms.HiddenInput(),
        }


class AddCompanyForm(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = ('game', 'name', 'cash', 'share_count')

        error_messages = {
            NON_FIELD_ERRORS: {'unique_together': DUPLICATE_COMPANY_ERROR},
        }

        widgets = {
            'game': forms.HiddenInput(),
        }
