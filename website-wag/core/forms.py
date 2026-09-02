from django import forms


class ContactLeadForm(forms.Form):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control form-control-highlight'}))
