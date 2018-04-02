from django import forms
from .models import Story, Response, Rating


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = [
            "title",
            "photo",
            "description",
            "content",
            "tag",
            "category",
            "draft",
        ]
        widgets = {
            "title": forms.TextInput(attrs={
                'class':'input',
                'required': 'True',
                'placeholder': 'Title',
            }),
            "photo": forms.ClearableFileInput(attrs={
                'class':'input',
                'placeholder': 'Image',
            }
            ),
            "description": forms.Textarea(attrs={
                'class':'input',
                'required':'true',
                'placeholder': 'Description',
            }
            ),
            "content": forms.Textarea(attrs={
                'class':'input',
                'required': 'True',
                'placeholder': 'Content',
            }
            ),
            "category": forms.TextInput(attrs={
                'class':'input',
                'required':'true',
                'placeholder': 'Categories',
            }),
            "draft": forms.CheckboxInput(attrs={
                'class':'input',
            }),

            "tag": forms.TextInput(attrs={
                'class':'input',
                'required':'true',
                'placeholder': 'Tags',
            }),



        }



class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = [
            "comment",
        ]

        widgets = {
            "comment": forms.TextInput(attrs={
                'class':'input',
                'required': 'True',
                'placeholder': 'Leave a Comment.....',
            }),
        }