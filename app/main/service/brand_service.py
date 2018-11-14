import datetime

from app.main import db
from app.main.model.brand_model import Brand
from app.main.service.synonym_service import add_synonym


class BrandServiceResponse:
    Success = 200
    Created = 201
    AlreadyExists = 400
    DoesNotExist = 404


def get_brands_by_account(account_id):
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


def update_brand(account_id, brand, change_data):
    # Check if there is an existing brand with the name
    existing = get_brand_by_name(account_id, change_data['name'])
    if existing and existing.id != brand.id:
        return dict(success=False,
                    message='Your account already has a brand with that name.'), BrandServiceResponse.AlreadyExists

    Brand.query.filter_by(id=brand.id).update(dict(name=change_data['name']))
    db.session.commit()

    return dict(success=True), BrandServiceResponse.Success


def create_brand(account_id, brand_data, create_synonym=True):
    existing = get_brand_by_name(account_id, brand_data['name'])

    if not existing:
        brand = Brand(name=brand_data['name'], created_at=datetime.datetime.utcnow(), account_id=account_id)

        db.session.add(brand)

        if create_synonym:
            db.session.flush()
            db.session.refresh(brand)

            # Add default synonym to the brand
            add_synonym(brand.id, {'synonym': brand.name})
        else:
            db.session.commit()

        return dict(success=True), BrandServiceResponse.Created
    else:
        return dict(success=False,
                    message='Your account already has a brand with that name.'), BrandServiceResponse.AlreadyExists
