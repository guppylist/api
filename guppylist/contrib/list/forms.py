from django import forms
from django.contrib.auth import get_user_model

from guppylist.contrib.list.models import List


class ListItemAddForm(forms.Form):
    url = forms.URLField(required=True, widget=forms.TextInput(
        attrs={
            'placeholder': 'http://example.com/',
            'class': 'form-control',
            'ng-model':'url',
            'ng-change':'urlChanged();',
        },
    ))

    title = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'placeholder': 'Title',
            'class': 'form-control',
            'ng-model': 'title',
        },
    ))

    description = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'placeholder': 'Description',
            'class': 'form-control',
            'ng-model': 'description',
        },
    ))

    image = forms.CharField(
        required=True,
        widget=forms.RadioSelect(
            # choices=(('h', 'hello'), ('w', 'world')),
            attrs={
                'ng-model': 'image',
            },
        ),
    )


"""
class ListAddNewForm(forms.Form):
    product_id = forms.CharField(required=True, widget=forms.HiddenInput(attrs={'ng-model': 'form.product_id'}))
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'List Name', 'ng-model': 'form.title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description', 'ng-model': 'form.description'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'My shoe size is 8 and I like the blue ones.', 'ng-model': 'form.notes'}))

class ListAddExistingForm(forms.Form):
    product_id = forms.CharField(required=True, widget=forms.HiddenInput(attrs={'ng-model': 'form.product_id'}))
    # list_id = forms.ChoiceField(required=True, choices=lists)
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'My shoe size is 8 and I like the blue ones.', 'ng-model': 'form.notes'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ListAddExistingForm, self).__init__(*args, **kwargs)

        # Get list choices.
        lists = [(list.id, list.title) for list in List.objects.filter(user=self.user)]
        self.fields['list_id'] = forms.ChoiceField(required=True, choices=lists)
"""