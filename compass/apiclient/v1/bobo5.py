# -*- coding:utf-8 -*-

from bobo3 import DBSession
from bobo3 import User

session = DBSession()
users = session.query(User).filter(User.name=='Bob').first()
print type(users)
print users
print users.id