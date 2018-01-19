# coding=utf-8
from django import forms
from django.core.validators import RegexValidator
from questions.models import Profile
from questions.models import Answer, Question, Tag

_alphanumeric_validator = RegexValidator(r'^[0-9a-zA-Z_]*$',
                                         "Only alphabetic symbols, numbers and underscores allowed")

# ENABLED FORMS


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

        # unique username validation
        if 'username' in cleaned_data:
            username = cleaned_data["username"]
            users_with_username = Profile.objects.filter(username=username)
            if len(users_with_username) > 0:
                raise forms.ValidationError("User with same username already registered")

        # password confirmation validation
        if 'password' in cleaned_data:
            password = cleaned_data["password"]
            confirm_password = cleaned_data["confirm_password"]
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match")
            return cleaned_data

    def save(self):
        new_profile = Profile(username=self.cleaned_data["username"],
                              email=self.cleaned_data["email"],
                              avatar=self.cleaned_data["avatar"])
        new_profile.set_password(self.cleaned_data["password"])
        new_profile.save()
        return new_profile


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
    
    def __init__(self, post=None,  user=None):
        super(AskForm, self).__init__(data=post)
        self.user = user

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

    def clean(self):
        cleaned_data = super(AskForm, self).clean()
        tag_list = cleaned_data["tags"].split(',')
        cleaned_data["tags"] = []

        for tag in tag_list:
            tag = tag.strip()
            if tag != u'':
                cleaned_data["tags"].append(tag)

        if not cleaned_data["tags"]:
            raise forms.ValidationError("Specify at least one valid tag")
        return cleaned_data

    def save(self):
        if self.user is not None:
            question = Question(user=self.user,
                                title=self.cleaned_data["title"],
                                text=self.cleaned_data["question"],
                                snippet=self.cleaned_data["question"][:100])
            question.save()
            #clean() guarantees that cleaned_data has at least one tag
            for tag in self.cleaned_data["tags"]:
                search_tag = Tag.objects.filter(name=tag).last()
                if search_tag:
                    question.tags.add(search_tag)
                else:
                    new_tag = Tag(name=tag)
                    new_tag.save()
                    question.tags.add(new_tag)

            question.save()
            return question


class AnswerForm(forms.Form):

    def __init__(self, post=None, user=None, question=None):
        super(AnswerForm, self).__init__(data=post)
        self.user = user
        self.question = question

    answer = forms.CharField(label="Answer",
                               widget=forms.Textarea(
                                   attrs={
                                       'class': 'form-control',
                                       'placeholder': 'Enter your answer here...'
                                   }
                               ))

    def save(self):
        new_answer = Answer(user=self.user,
                            question=self.question,
                            text=self.cleaned_data["answer"])
        new_answer.save()


class ProfileForm(forms.Form):

    profile_edited = None

    def __init__(self, post=None, files=None, profile_edited=None, initial=None):
        super(ProfileForm, self).__init__(data=post, files=files, initial=initial)
        self.profile_edited = profile_edited


    username = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Name, displayed to other users'}
    ), validators=[_alphanumeric_validator])
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(
        attrs={'class': 'form-control',
               'placeholder': 'your@email.com'}
    ))

    avatar = forms.ImageField(required=False,
                              widget=forms.FileInput(
                                  attrs={'class': 'form-control-file'}
                                )
                              )

    def clean_username(self):
        username = self.cleaned_data["username"]
        users_with_username = Profile.objects.filter(username=username)
        if len(users_with_username) > 0 and self.profile_edited.username != username:
            self.add_error(None, "User with username " + username + " already exists")
            return self.profile_edited.username
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        users_with_email = Profile.objects.filter(email=email)
        if len(users_with_email) > 0 and self.profile_edited.email != email:
            # it means that there is some other user with selected email
            self.add_error(None, "User with email " + email + " already exists")
            return self.profile_edited.email
        return email


# TUTORIAL FORMS
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