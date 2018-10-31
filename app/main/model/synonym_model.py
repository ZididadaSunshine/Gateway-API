from app.main import db


class Synonym(db.Model):
    """ SQLAlchemy model for brand synonyms. """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # To avoid redundancy, synonyms are unique
    synonym = db.Column(db.String(255), unique=True, nullable=False)

