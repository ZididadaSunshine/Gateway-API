from flask import request
from flask_restplus import Resource

from app.main.decorator.auth_decorator import auth_required
from app.main.dto.brand_dto import BrandDTO
from app.main.service.authorization_service import get_account_id
from app.main.service.brand_service import get_brands_from_account, create_brand, BrandServiceResponse, get_brand_by_id, \
    delete_brand, update_brand
from app.main.service.synonym_service import add_synonym, get_synonyms, delete_synonym

api = BrandDTO.api


@api.route('')
class BrandsResource(Resource):
    @api.doc('Retrieves a list of all the brands associated with the authorized account.', security='jwt')
    @api.marshal_list_with(BrandDTO.brand)
    @auth_required(api)
    def get(self):
        return get_brands_from_account(get_account_id())

    @api.response(BrandServiceResponse.Created, 'Brand successfully created.')
    @api.response(BrandServiceResponse.AlreadyExists, 'The authorized account already has a brand with that name.')
    @api.expect(BrandDTO.brand, validate=True)
    @api.doc('Create a new brand to be associated with the authorized account.', security='jwt')
    @auth_required(api)
    def post(self):
        return create_brand(get_account_id(), request.json)


@api.route('/<int:brand_id>')
@api.param('brand_id', 'A brand identifier associated with the authorized account.')
@api.response(BrandServiceResponse.DoesNotExist, 'The requested brand does not exist.')
class BrandResource(Resource):
    @api.response(BrandServiceResponse.Success, 'The brand was successfully deleted.')
    @api.response(BrandServiceResponse.DoesNotExist, 'The requested brand does not exist.')
    @api.doc('Delete the brand.', security='jwt')
    @auth_required(api)
    def delete(self, brand_id):
        brand = get_brand_by_id(get_account_id(), brand_id)

        if not brand:
            api.abort(BrandServiceResponse.DoesNotExist)

        delete_brand(brand)

        return dict(success=True)

    @api.doc('Retrieve details about the brand.', security='jwt')
    @api.response(BrandServiceResponse.DoesNotExist, 'The requested brand does not exist.')
    @api.marshal_with(BrandDTO.brand)
    @auth_required(api)
    def get(self, brand_id):
        brand = get_brand_by_id(get_account_id(), brand_id)

        if not brand:
            api.abort(BrandServiceResponse.DoesNotExist)

        return brand

    @api.response(BrandServiceResponse.Success, 'Brand details updated successfully.')
    @api.response(BrandServiceResponse.AlreadyExists, 'The brand cannot be renamed to an existing brand.')
    @api.response(BrandServiceResponse.DoesNotExist, 'The requested brand does not exist.')
    @api.doc('Update details about the brand.', security='jwt')
    @api.expect(BrandDTO.brand, validate=True)
    @auth_required(api)
    def put(self, brand_id):
        brand = get_brand_by_id(get_account_id(), brand_id)

        if not brand:
            api.abort(BrandServiceResponse.DoesNotExist)

        return update_brand(account_id=get_account_id(), brand=brand, data=request.json)


@api.route('/<int:brand_id>/synonyms')
@api.param('brand_id', 'A brand identifier associated with the authorized account.')
class BrandSynonymsResource(Resource):
    @api.response(BrandServiceResponse.DoesNotExist, 'The requested brand does not exist.')
    @api.doc('Retrieve all synonyms associated with the brand.', security='jwt')
    @auth_required(api)
    def get(self, brand_id):
        brand = get_brand_by_id(get_account_id(), brand_id)

        if not brand:
            api.abort(BrandServiceResponse.DoesNotExist)

        synonyms = get_synonyms(brand.id)

        # Instead of returning the model for each synonym, we just return the synonym itself
        return [synonym.synonym for synonym in synonyms]

    @api.response(BrandServiceResponse.DoesNotExist, 'The requested brand does not exist.')
    @api.expect(BrandDTO.synonym, validate=True)
    @api.doc('Create a new synonym to be associated with the brand.', security='jwt')
    @auth_required(api)
    def post(self, brand_id):
        brand = get_brand_by_id(get_account_id(), brand_id)

        if not brand:
            api.abort(BrandServiceResponse.DoesNotExist)

        return add_synonym(brand.id, request.json)


@api.route('/<int:brand_id>/synonyms/<string:synonym>')
class BrandSynonymResource(Resource):
    @api.response(BrandServiceResponse.DoesNotExist, 'The requested brand does not exist.')
    @api.doc('Delete a synonym\'s association with a brand.', security='jwt')
    @auth_required(api)
    def delete(self, brand_id, synonym):
        brand = get_brand_by_id(get_account_id(), brand_id)

        if not brand:
            api.abort(BrandServiceResponse.DoesNotExist)

        return delete_synonym(brand_id, synonym)
