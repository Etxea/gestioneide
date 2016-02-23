# -*- coding: utf-8 -*-

from django import forms


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )
class OldDatabaseForm(forms.Form):
    dbfile = forms.FileField(
        label='Select a file'
    )
