from flask_peewee.utils import check_password
from flask_sqlalchemy import Model
from sqlalchemy import Column, Integer, String, DateTime


class Account(Model):
    """ SQLAlchemy model for accounts. """

    id = Column(Integer, primary_key=True, autoincrement=True)
    creation_date = Column(DateTime, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    password = Column(String(255))

    """ Check if a password matches the hashed password stored for the account. """
    def check_password(self, password):
        return check_password(self.password, password)

    def __repr__(self):
        return f"<User {self.email}'>"
