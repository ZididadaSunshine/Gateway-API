import datetime

from sqlalchemy import and_

from app.main import db
from app.main.model.brand_model import Brand


class BrandServiceResponse:
    Success = 200
    Created = 201
    AlreadyExists = 400


def get_brands_from_account(account_id):
    brands = Brand.query.filter_by(account_id=account_id).all()

    return brands


def create_brand(account_id, data):
    existing = Brand.query.filter((Brand.account_id == account_id) & (Brand.name == data['name'])).first()

    if not existing:
        brand = Brand(name=data['name'], creation_date=datetime.datetime.utcnow(), account_id=account_id)

        db.session.add(brand)
        db.session.commit()

        return dict(message='Brand successfully created.'), BrandServiceResponse.Created
    else:
        return dict(message=f'Your account already has a brand with that name.'), BrandServiceResponse.AlreadyExists
