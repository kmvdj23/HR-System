import random, string
from werkzeug import security

def choices_from_dict(source, prepend_blank=True):
    choices = list()

    if prepend_blank:
        choices.append(('', 'Please select one...'))

    for key, value in source.items():
        pair = (key, value)
        choices.append(pair)

    return choices


def choices_from_list(source, prepend_blank=True):
    choices = list()

    if prepend_blank:
        choices.append(('', 'Please select one...'))

    for item in source:
        pair = (item, item)
        choices.append(pair)

    return choices


def generate_random_password(len=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=len))


def password_encrypt(raw_password):
    return security.generate_password_hash(raw_password, method='pbkdf2:sha256', salt_length=8)

def password_decrypt(input_password, encrypted_password):
    return security.check_password_hash(encrypted_password, input_password)