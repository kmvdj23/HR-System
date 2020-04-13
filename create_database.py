from app.config import db
from app.models import Account
from lib import password_encrypt

db.drop_all()
db.create_all()

account1 = Account(first_name='Kristopher Matthew',
                last_name='De Jesus',
                username='kmvdj23',
                email='kristophermatthewdejesus@gmail.com',
                mobile='09167312622',
                password=password_encrypt('kristopher@23'),
                role='it')

account2 = Account(first_name='Katherine',
                last_name='Domingo',
                username='katdom13',
                email='katdom13@gmail.com',
                mobile='09174167279',
                password=password_encrypt('Homestuck1998'),
                role='admin')

db.session.add(account1)
db.session.add(account2)
db.session.commit()

