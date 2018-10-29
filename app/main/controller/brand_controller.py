from flask import request
from flask_restplus import Resource

from app.main.decorators.authorization_decorator import require_authorization
from app.main.dto.brand_dto import BrandDTO
from app.main.service.authorization_service import get_account_id
from app.main.service.brand_service import get_brands_from_account, create_brand, BrandServiceResponse

api = BrandDTO.api


@api.route('')
class BrandsResource(Resource):
    @api.doc('Retrieves a list of all the brands associated with the authorized account.', security='jwt')
    @require_authorization
    def get(self):
        # todo: serialize
        return get_brands_from_account(get_account_id())

    @api.response(BrandServiceResponse.Created, 'Brand successfully created.')
    @api.response(BrandServiceResponse.AlreadyExists, 'The authorized account already has a brand with that name.')
    @api.expect(BrandDTO.new_brand, validate=True)
    @api.doc('Create a new brand to be associated with the authorized account.', security='jwt')
    @require_authorization
    def post(self):
        return create_brand(get_account_id(), request.json)


@api.route('/<id>')
@api.doc(params={'id': 'A brand identifier associated with the authorized account.'})
class BrandResource(Resource):
    @api.doc('Delete the brand.', security='jwt')
    def delete(self):
        pass

    @api.doc('Retrieve details about the brand.', security='jwt')
    def get(self):
        pass

    @api.doc('Update details about the brand.', security='jwt')
    def put(self):
        pass
