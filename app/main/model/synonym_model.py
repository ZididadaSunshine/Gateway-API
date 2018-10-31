from app.main import db


class Synonym(db.Model):
    """ SQLAlchemy model for brand synonyms. """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creation_date = db.Column(db.DateTime, nullable=False)
    synonym = db.Column(db.String(255), unique=True, nullable=False)
