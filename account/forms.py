from django import forms
from django.contrib.auth.models import User
from .models import Author, Message


class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'required': 'true',
            'placeholder': 'Password'
        }))

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={
                'class': 'input',
                'required': 'true',
                'placeholder': 'First Name',
            }
            ),
            "last_name": forms.TextInput(attrs={
                'class': 'input',
                'required': 'true',
                'placeholder': 'Last Name',
            }
            ),
            "username": forms.TextInput(attrs={
                'class': 'input',
                'required': 'true',
                'placeholder': 'Username',
            }
            ),
            "email": forms.TextInput(attrs={
                'class': 'input',
                'required': 'true',
                'placeholder': 'example@example.com',
            }
            ),
        }


class SigninForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input',
            'required': 'true',
            'placeholder': 'Username',
        }))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'required': 'true',
            'placeholder': 'Password'
        }))

    class Meta:
        fields = [
            "username",
            "password",
        ]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={
                'class':'input',
                'required': 'true',
                'placeholder': 'First Name',
            }
            ),
            "last_name": forms.TextInput(attrs={
                'class':'input',
                'required': 'true',
                'placeholder': 'Last Name',
            }
            ),
            "email": forms.TextInput(attrs={
                'class':'input',
                'required': 'true',
                'placeholder': 'example@example.com',
            }
            ),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = [
            "bio",
            "photo",
            "dob",
            "gender",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={
                'class':'input',
                'placeholder': 'Bio',
            }
            ),
            "photo": forms.FileInput(attrs={
                'class':'input',
                'placeholder': 'Image',
            }
            ),
            "dob": forms.DateInput(attrs={
                'class':'input',
                'required': 'true',
                'placeholder': 'YYYY-MM-DD',
            }
            ),
            "gender": forms.Select(attrs={
                'class':'input',
                'required': 'true',
                'placeholder': 'Gender'
            })
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                'class':'input',
                'required': 'true',
                'placeholder': 'Message'
            }),
        }
