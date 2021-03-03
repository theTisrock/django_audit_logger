from django import forms
from .models import ListItem


class ListItemForm(forms.ModelForm):
    class Meta:
        model = ListItem
        fields = ['item', 'complete']


class EditItemForm(forms.ModelForm):
    class Meta:
        model = ListItem
        fields = ['item']

# end
