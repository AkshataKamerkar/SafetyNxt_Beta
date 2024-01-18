from django import forms
from .models import Contact, Route

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['fname', 'lname', 'email', 'mob', 'msg']


class RouteFrom(forms.Form):

    start = forms.CharField(label='Start Location', max_length=100, widget=forms.TextInput(attrs={'id': 'id_start_location'}))
    destination = forms.CharField(label='End Location', max_length=100, widget=forms.TextInput(attrs={'id': 'id_end_location'}))

