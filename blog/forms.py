from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'text')

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'placeholder': 'Enter name', 'class': 'form-control'}
        self.fields['email'].widget.attrs = {'placeholder': 'Enter email', 'class': 'form-control'}
        self.fields['text'].widget.attrs = {'placeholder': 'Comment here...', 'class': 'form-control', 'rows': '5'}


class ContactForm(forms.Form):
    subject = forms.CharField(label='Subject', widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Text', widget=forms.Textarea(attrs={'class': 'form-control', "rows": 5}))
    from_email = forms.EmailField(required=True)


class EmailBlogForm(forms.Form):
    name = forms.CharField(label='Name', max_length=25)
    email = forms.EmailField(required=True)
    to = forms.EmailField(required=True)
    comments = forms.CharField(label='Text', widget=forms.Textarea(attrs={'class': 'form-control', "rows": 5}))
