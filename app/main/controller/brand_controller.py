from flask import request
from flask_restplus import Resource

from app.main.dto.brand_dto import BrandDTO
from app.main.service.authorization_service import get_account_id, get_is_authorized, AuthorizationResponse
from app.main.service.brand_service import get_brands_from_account, create_brand, BrandServiceResponse, get_brand_by_id, \
    delete_brand

api = BrandDTO.api


@api.route('')
class BrandsResource(Resource):
    @api.doc('Retrieves a list of all the brands associated with the authorized account.', security='jwt')
    @api.marshal_list_with(BrandDTO.brand)
    def get(self):
        if not get_is_authorized():
            api.abort(AuthorizationResponse.Unauthorized)

        return get_brands_from_account(get_account_id())

    @api.response(BrandServiceResponse.Created, 'Brand successfully created.')
    @api.response(BrandServiceResponse.AlreadyExists, 'The authorized account already has a brand with that name.')
    @api.expect(BrandDTO.brand, validate=True)
    @api.doc('Create a new brand to be associated with the authorized account.', security='jwt')
    def post(self):
        if not get_is_authorized():
            api.abort(AuthorizationResponse.Unauthorized)

        return create_brand(get_account_id(), request.json)


@api.route('/<int:public_id>')
@api.param('public_id', 'A brand identifier associated with the authorized account.')
class BrandResource(Resource):
    @api.response(BrandServiceResponse.Success, 'The brand was successfully deleted.')
    @api.response(BrandServiceResponse.DoesNotExist, 'The requested brand does not exist.')
    @api.doc('Delete the brand.', security='jwt')
    def delete(self, public_id):
        if not get_is_authorized():
            api.abort(AuthorizationResponse.Unauthorized)

        brand = get_brand_by_id(get_account_id(), public_id)

        if not brand:
            api.abort(BrandServiceResponse.DoesNotExist)

        delete_brand(brand)

        return dict(success=True)

    @api.response(BrandServiceResponse.DoesNotExist, 'The requested brand does not exist.')
    @api.doc('Retrieve details about the brand.', security='jwt')
    @api.marshal_with(BrandDTO.brand)
    def get(self, public_id):
        if not get_is_authorized():
            api.abort(AuthorizationResponse.Unauthorized)

        brand = get_brand_by_id(get_account_id(), public_id)

        if not brand:
            api.abort(BrandServiceResponse.DoesNotExist)

        return brand

    @api.response(BrandServiceResponse.Success, 'Brand details updated successfully.')
    @api.response(BrandServiceResponse.AlreadyExists, 'The brand cannot be renamed to an existing brand.')
    @api.doc('Update details about the brand.', security='jwt')
    def put(self, public_id):
        if not get_is_authorized():
            api.abort(AuthorizationResponse.Unauthorized)

        # TODO
         
        pass


@api.route('/<int:public:id>/synonym')
@api.param('public_id', 'A brand identifier associated with the authorized account.')
class SynonymsResource(Resource):
    @api.doc('Retrieve all synonyms associated with the brand.', security='jwt')
    def get(self, public_id):
        if not get_is_authorized():
            api.abort(AuthorizationResponse.Unauthorized)

        brand = get_brand_by_id(get_account_id(), public_id)

        if not brand:
            api.abort(BrandServiceResponse.DoesNotExist)
