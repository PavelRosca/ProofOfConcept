from django import forms
from django.core.validators import RegexValidator

FORM_CONTROL = {'class': 'form-control'}

POSTAL_CODE_VALIDATOR = RegexValidator(r'^\d{5}$', 'Inserisci un CAP valido di 5 cifre.')
PROVINCE_VALIDATOR = RegexValidator(r'^[A-Za-z]{2}$', 'Inserisci la sigla provincia di 2 lettere (es. RM).')
OTP_CODE_VALIDATOR = RegexValidator(r'^\d{6}$', 'Inserisci il codice a 6 cifre ricevuto via email.')


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs=FORM_CONTROL))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs=FORM_CONTROL))
    # Capped at 150, not EmailField's usual 254 — otp_obj.email becomes User.username
    # on verify (max_length=150), and plain (non-Model) forms don't inherit that cap.
    email = forms.EmailField(max_length=150, widget=forms.EmailInput(attrs=FORM_CONTROL))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs=FORM_CONTROL))
    address_street = forms.CharField(max_length=200, widget=forms.TextInput(attrs=FORM_CONTROL))
    address_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs=FORM_CONTROL))
    address_postal_code = forms.CharField(
        max_length=10, validators=[POSTAL_CODE_VALIDATOR], widget=forms.TextInput(attrs=FORM_CONTROL)
    )
    address_city = forms.CharField(max_length=100, widget=forms.TextInput(attrs=FORM_CONTROL))
    address_province = forms.CharField(
        max_length=2, validators=[PROVINCE_VALIDATOR], widget=forms.TextInput(attrs=FORM_CONTROL)
    )

    def clean_email(self):
        # Deliberately does NOT check whether the email is already registered here —
        # doing so would let an anonymous visitor enumerate party members by email
        # (political affiliation is sensitive data). The already-registered case is
        # instead handled indistinguishably in the view, see register_submit().
        return self.cleaned_data['email'].strip().lower()

    def clean_address_province(self):
        return self.cleaned_data['address_province'].strip().upper()


class OTPVerifyForm(forms.Form):
    code = forms.CharField(
        min_length=6,
        max_length=6,
        validators=[OTP_CODE_VALIDATOR],
        widget=forms.TextInput(attrs={
            **FORM_CONTROL,
            'inputmode': 'numeric',
            'autocomplete': 'one-time-code',
        }),
    )
