from django import forms
from app.models import *
from django.forms import ValidationError
from django.contrib.auth import login, get_user


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)

    def clean_username(self):
        user = Profile.objects.filter(user__username=self.cleaned_data['username']).first()
        if user is not None:
            raise ValidationError('Such username is already exist')
        return self.cleaned_data['username']

    def clean_repeat_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['repeat_password']:
            raise ValidationError('Passwords doesn\'t match')
        return self.cleaned_data['repeat_password']


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'login', 'placeholder': 'Макс. 20 сим.', 'class': 'input_style'}),
        max_length=20)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password', 'class': 'input_style'}))


class AskForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'По чему плавают утки?'}), max_length=256)
    text = forms.CharField(widget=forms.Textarea(
        attrs={'id': 'questionText', 'rows': '3', 'placeholder': 'Спать не могу, только об этом и думаю'}),
        max_length=DEFAULT_TEXT_LENGTH)
    tags = forms.CharField(widget=forms.TextInput(attrs={'id': 'inputTags', 'placeholder': 'Макс. длина тега 32 сим.'}))

    def clean_tags(self):
        tags = self.cleaned_data['tags'].split(',')
        for tag in tags:
            if len(tag.rstrip().lstrip()) > 32:
                raise ValidationError('The maximum length of one tag is 32 characters')

        return self.cleaned_data['tags']


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'floatingTextarea2'}),
                           max_length=DEFAULT_TEXT_LENGTH)


class EditProfileForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.EmailField()
    new_password = forms.CharField(widget=forms.PasswordInput, required=False)
    repeat_new_password = forms.CharField(widget=forms.PasswordInput, required=False)
    avatar = forms.ImageField(required=False)

    def clean_repeat_new_password(self):
        if self.cleaned_data['new_password'] != self.cleaned_data['repeat_new_password']:
            raise ValidationError('Passwords doesn\'t match')
        return self.cleaned_data['repeat_new_password']
