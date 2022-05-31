from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserCreateForm(UserCreationForm):
    """
    Customized user creation form
    Remover help_text from input fields in html
    """

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'first_name',
                          'last_name', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class SignUpForm(UserCreateForm):
    """Registration user form"""
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]
