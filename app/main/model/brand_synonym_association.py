from app.main import db


class BrandSynonym(db.Model):
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), primary_key=True)
    synonym_id = db.Column(db.Integer, db.ForeignKey('synonym.id'), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=True)
