from app.config import db
from app.models import Account, Status

db.drop_all()
db.create_all()

account = Account(first_name='Kristopher Matthew',last_name='De Jesus',password='kristopher@23',account_type=0,username='kmvdj23',mobile_number='09167312622')
account1 = Account(first_name='Katherine',last_name='Domingo',password='Homestuck1998',account_type=0,username='katdom13',mobile_number='09174167279')

status = Status(name='Pending')
status2 = Status(name='Phone Invite')
status3 = Status(name="Can't be reached")
status4 = Status(name='Declined')
status5 = Status(name='For Interview')
status6 = Status(name='Passed')
status7 = Status(name='Failed')
status8 = Status(name='Hired')

db.session.add(account)
db.session.add(account1)
db.session.add(status,status2,status3,status4,status5,status6,status7,status8)
db.session.commit()

