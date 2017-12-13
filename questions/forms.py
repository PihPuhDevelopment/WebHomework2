# coding=utf-8
from django import forms
from django.core.validators import RegexValidator
from questions.models import Profile
from questions.models import Answer

_alphanumeric_validator = RegexValidator(r'^[0-9a-zA-Z_]*$',
                                         "Only alphabetic symbols, numbers and underscores allowed")


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Name, displayed to other users'}
    ), validators=[_alphanumeric_validator])
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(
        attrs={'class': 'form-control',
               'placeholder': 'your@email.com'}
    ))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'placeholder': '***********'}
    ))
    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'placeholder': '***********'}
    ))

    avatar = forms.ImageField(
        widget=forms.FileInput(
            attrs={'class': 'form-control-file'}
        )
    )

    def clean(self):
        # unique email validation
        cleaned_data = super(RegisterForm, self).clean()
        if 'email' in cleaned_data:
            email = cleaned_data["email"]
            users_with_email = Profile.objects.filter(email=email)
            if len(users_with_email) > 0:
                raise forms.ValidationError("User with same email already registered")

        # password confirmation validation
        if 'password' in cleaned_data:
            password = cleaned_data["password"]
            confirm_password = cleaned_data["confirm_password"]
            if not password == confirm_password:
                raise forms.ValidationError("Passwords do not match")
            return cleaned_data

    def save(self):
        new_profile = Profile(username=self.cleaned_data["username"],
                              email=self.cleaned_data["email"],
                              avatar=self.cleaned_data["avatar"])
        new_profile.set_password(self.cleaned_data["password"])
        new_profile.save()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Name, displayed to other users'}
    ), validators=[_alphanumeric_validator])
    password = forms.CharField(max_length=128, widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'placeholder': '***********'}
    ))


class AskForm(forms.Form):
    title = forms.CharField(max_length=100, label="Title", help_text="Clear and short statement of your problem",
                            widget=forms.TextInput(
                                attrs={'class': 'form-control',
                                       'placeholder': 'Enter question title'}
                            ))
    question = forms.CharField(label="Question", help_text="Detailed explanation of your problem",
                               widget=forms.Textarea(
                                   attrs={
                                       'class': 'form-control',
                                       'placeholder': 'Enter your question'
                                   }
                               ))
    tags = forms.CharField(label="Tags", help_text="List of tags, separated by commas",
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control',
                                   'placehoolder': 'tag1, tag2, etc...'
                               }
                           ))


class AuthorForm(forms.Form):
    name = forms.CharField(max_length=255)
    birthday = forms.DateField(
        help_text="Enter your birthday",
        widget=forms.TextInput(attrs={'class': 'text-input'})
    )

    def clean_name(self):
        name = self.cleaned_data["name"]
        raise forms.ValidationError(u"Рюзке симболы!!! Карамба!")

    def clean(self):
        raise forms.ValidationError(u"Dichara!!!")

    def save(self):
        pass


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = []


class ProfileForm(forms.Form):
    avatar = forms.ImageField(
        widget=forms.FileInput(
            attrs={'class': 'form-control-file'}
        )
    )
