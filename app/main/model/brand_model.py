from app.main import db
from app.main.model import brand_synonym_association


class Brand(db.Model):
    """ Model for brands. """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creation_date = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    synonyms = db.relationship("Synonym", secondary=brand_synonym_association, back_populates="brands")

    def __repr__(self):
        return f"<Brand {self.name}'>"
