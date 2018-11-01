from app.main import db
from app.main.model.brand_synonym_association import BrandSynonym


class Synonym(db.Model):
    """ SQLAlchemy model for brand synonyms. """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # To avoid redundancy, synonyms are unique
    synonym = db.Column(db.String(255), unique=True, nullable=False)
    brands = db.relationship("Brand", secondary=BrandSynonym.__table__, back_populates="synonyms")
