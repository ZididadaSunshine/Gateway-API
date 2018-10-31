import datetime

from app.main import db
from app.main.model.brand_model import Brand


class BrandServiceResponse:
    Success = 200
    Created = 201
    AlreadyExists = 400
    DoesNotExist = 404


def get_brands_from_account(account_id):
    brands = Brand.query.filter_by(account_id=account_id).all()

    return brands


def get_brand_by_id(account_id, brand_id):
    return Brand.query.filter((Brand.account_id == account_id) & (Brand.id == brand_id)).first()


def get_brand_by_name(account_id, name):
    return Brand.query.filter((Brand.account_id == account_id) & (Brand.name.ilike(name))).first()


def delete_brand(brand):
    db.session.delete(brand)
    db.session.commit()

    return dict(success=True), BrandServiceResponse.Success


def update_brand(account_id, brand, data):
    # Check if there is an existing brand with the name
    existing = get_brand_by_name(account_id, data['name'])
    if existing and existing.id != brand.id:
        return dict(success=True,
                    message='You already have a brand with that name.'), BrandServiceResponse.AlreadyExists

    Brand.query.filter_by(id=brand.id).update(dict(name=data['name']))
    db.session.commit()

    return dict(success=True), BrandServiceResponse.Success


def create_brand(account_id, data):
    existing = get_brand_by_name(account_id, data['name'])

    if not existing:
        brand = Brand(name=data['name'], creation_date=datetime.datetime.utcnow(), account_id=account_id)

        db.session.add(brand)
        db.session.commit()

        return dict(success=True), BrandServiceResponse.Created
    else:
        return dict(success=False,
                    message=f'Your account already has a brand with that name.'), BrandServiceResponse.AlreadyExists
