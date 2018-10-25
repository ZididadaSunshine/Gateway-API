import flask_bcrypt
from sqlalchemy import Column, Integer, String, DateTime

from app.main import database


class Account(database.Model):
    """ SQLAlchemy model for accounts. """

    id = Column(Integer, primary_key=True, autoincrement=True)
    creation_date = Column(DateTime, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    password = Column(String(255))

    """ Hashes and sets a cleartext password for the account. """
    def set_password(self, password):
        self.password = flask_bcrypt.generate_password_hash(password)

    """ Check if a password matches the hashed password stored for the account. """
    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.email}'>"
