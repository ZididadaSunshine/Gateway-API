import flask_bcrypt

from app.main import db


class Account(db.Model):
    """ SQLAlchemy model for accounts. """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    brands = db.relationship('Brand', backref='brand', lazy=True)

    """ Hashes and sets a password for the account. """
    def set_password(self, password):
        self.password = flask_bcrypt.generate_password_hash(password)

    """ Check if a password matches the hashed password stored for the account. """
    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"<Account {self.email}'>"
