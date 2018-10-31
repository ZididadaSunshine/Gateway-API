from sqlalchemy import Table

from app.main import db

brand_synonym_association = db.Table('brand_synonym', db.metadata,
                                     db.Column('brand_id', db.Integer, db.ForeignKey('brand.id')),
                                     db.Column('synonym_id', db.Integer, db.ForeignKey('synonym.id')),
                                     db.Column('created_at', db.DateTime, nullable=False))
