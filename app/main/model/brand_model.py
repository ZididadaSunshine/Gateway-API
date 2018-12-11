from app.main import db
from app.main.model.brand_synonym_association import BrandSynonym


class Brand(db.Model):
    """ Model for brands. """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(255), nullable=False, index=True)
    sentiment_average = db.Column(db.Float, nullable=True)
    sentiment_trend = db.Column(db.Float, nullable=True)
    posts = db.Column(db.Integer, nullable=True)
    statistics_updated_at = db.Column(db.DateTime, nullable=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    synonyms = db.relationship("Synonym", BrandSynonym.__table__, back_populates="brands")

    def __repr__(self):
        return f"<Brand {self.name}'>"
