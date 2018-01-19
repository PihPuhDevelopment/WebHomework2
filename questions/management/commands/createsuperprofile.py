from django.core.management.base import BaseCommand, CommandError
from questions.models import Profile
import re


def re_filter(regexp, user_input):
    match_result = re.match(regexp, user_input)
    if match_result:
        return True
    return False


def username_filter(user_input):
    return re_filter(r'^[a-zA-Z@.+-_0-9]+$', user_input)


def email_filter(user_input):
    return re_filter(r'^[^@]+@[^@]+\.[^@]+$', user_input)


def password_filter(user_input):
    return re_filter(r'^.+$', user_input)


def get_choice(filter, message, error_message):
    user_input = raw_input(message)
    while not filter(user_input):
        print('\033[91m'+error_message + '\033[0m')
        user_input = raw_input(message)
    return user_input


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            username = get_choice(username_filter, 'Username: ',
                                  "Username should contain only letters, numbers and @/./+/- symbols")
            email = get_choice(email_filter, 'Email: ', "Enter valid email")
            password = get_choice(password_filter, 'Password: ', "Enter valid password")
            password_confirm = get_choice(password_filter, 'Password: ', "Enter valid password")
            while password != password_confirm:
                print('\033[91m' + 'Passwords do not match')
                password = get_choice(password_filter, 'Password: ', "Enter valid password")
                password_confirm = get_choice(password_filter, 'Password: ', "Enter valid password")

            profile = Profile(username=username, email=email, avatar='uploads/admin.jpg')
            profile.set_password(password)
            profile.save()
        except KeyboardInterrupt:
            print('\033[91m'+'\nTerminated')