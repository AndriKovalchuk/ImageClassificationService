from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import (CharField, EmailField, EmailInput, PasswordInput,
                          TextInput)


class RegistrationForm(UserCreationForm):
    username = CharField(max_length=150, min_length=3, required=True,
                         widget=TextInput(attrs={"class": "form-control"}))

    email = EmailField(max_length=254, required=True,
                       widget=EmailInput(attrs={"class": "form-control"}))

    password1 = CharField(
        label="Password",
        required=True,
        widget=PasswordInput(attrs={"class": "form-control"})
    )

    password2 = CharField(
        label="Confirm Password",
        required=True,
        widget=PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class UserEditForm(UserChangeForm):
    current_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'current_password', 'new_password1', 'new_password2']

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if not self.instance.check_password(current_password):
            self.add_error('current_password', 'Current password is incorrect.')

        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error('new_password2', 'New passwords do not match.')

        return cleaned_data
