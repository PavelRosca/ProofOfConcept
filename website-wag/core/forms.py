from django import forms


class ContactLeadForm(forms.Form):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control form-control-highlight'}))
    # Honeypot: real users never see/fill this (hidden off-screen in the
    # template); a non-empty value means a bot filled every input it found.
    website = forms.CharField(required=False, widget=forms.HiddenInput)
