import random, string
import os
from werkzeug import security
from werkzeug.utils import secure_filename
<<<<<<< HEAD
=======
from flask_wtf import Form
>>>>>>> dd5d99f60e765caddf8e2f2e98eb7f869110e57a

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


def validate_file(csv_file):
    return os.path.splitext(csv_file)[1] in ['.csv']

<<<<<<< HEAD
=======

>>>>>>> dd5d99f60e765caddf8e2f2e98eb7f869110e57a
def upload_file(file, **kwargs):

    if file != '':
        filename = secure_filename(file.filename)

        if filename.endswith('.csv'):
            directory = os.path.join(os.getcwd(), 'app', 'uploads', 'csv', filename)
            file.save(directory)
            return directory

        elif filename.endswith(('.jpeg', '.jpg','.png')):
            user = kwargs.get('user')
<<<<<<< HEAD
            if not os.path.exists(os.path.join(os.getcwd(), 'app', 'uploads', 'pictures', user.username)):
                os.mkdir(os.path.join(os.getcwd(), 'app', 'uploads', 'pictures', user.username))
            directory = os.path.join(os.getcwd(), 'app', 'uploads', 'pictures', user.username, filename)
            file.save(directory)
            return directory
=======
            if not os.path.exists(os.path.join(os.getcwd(), 'app', 'static', 'images', user.username)):
                os.mkdir(os.path.join(os.getcwd(), 'app', 'static', 'images', user.username))
            directory = os.path.join(os.getcwd(), 'app', 'static', 'images', user.username, filename)
            file.save(directory)
            return os.path.join('static', 'images', user.username, filename)


class ModelForm(Form):
    def __init__(self, obj=None, prefix='', **kwargs):
        Form.__init__(
            self, obj=obj, prefix=prefix, **kwargs
        )
        self._obj = obj
>>>>>>> dd5d99f60e765caddf8e2f2e98eb7f869110e57a
