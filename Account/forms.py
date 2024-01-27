from django import forms
from .models import DuberUser
from django.contrib import messages


class DuberUserRegistrationForm(forms.ModelForm):
    use_required_attribute = False

    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password'
        })
    )
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password again'
        })
    )
    class Meta:
        model = DuberUser
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone_number']

    def __init__(self, *args, **kwargs):
        super(DuberUserRegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(DuberUserRegistrationForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords are not identical")
        return cleaned_data
