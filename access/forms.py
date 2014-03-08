from django import forms

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _


class UserRegisterForm(forms.ModelForm):
    """
    A form that creates a user. This is a modified version of Django's
    UserCreationForm.
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w]+$',
        error_messages={
            'invalid': _("Letters, digits and underscores (_) only.")})
    password1 = forms.RegexField(label=_("Password"), min_length=8,
        regex=r'[(?=.\d)]',
        widget=forms.PasswordInput,
        error_messages={
            'invalid': _("Passwords must be at least 8 characters long and include at least 1 digit.")})
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput)
    email = forms.EmailField(label=_("Email"),
        error_messages={
            'invalid': _("This must be a valid email address.")})

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_email(self):
        email = self.cleaned_data["email"]
        return email

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

