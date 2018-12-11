from flask import request
from flask_restplus import Resource

from app.main.controller.authorization_controller import auth_required, get_token
from app.main.dto.brand_dto import BrandDTO
from app.main.dto.synonym_dto import SynonymDTO
from app.main.service.authorization_service import get_account_id

import app.main.service.synonym_service as synonym_service
import app.main.service.brand_service as brand_service
from app.main.service.statistics_service import get_brand_sentiment

api = BrandDTO.api


@api.route('')
class BrandsResource(Resource):
    @api.doc('Retrieves a list of all the brands associated with the authorized account.', security='jwt')
    @auth_required(api)
    def get(self):
        results = []

        for brand in brand_service.get_brands_by_account(get_account_id(get_token())):
            sentiment = get_brand_sentiment(brand)
            results.append({'id': brand.id, 'name': brand.name, 'average': sentiment['average'],
                            'trend': sentiment['trend']})

        return results

    @api.response(brand_service.BrandServiceResponse.Created, 'Brand successfully created.')
    @api.response(brand_service.BrandServiceResponse.AlreadyExists, 'The authorized account already has a brand with that name.')
    @api.expect(BrandDTO.brand, validate=True)
    @api.doc('Create a new brand to be associated with the authorized account.', security='jwt')
    @auth_required(api)
    def post(self):
        if not request.json['name'].strip():
            api.abort(400)

        return brand_service.create_brand(get_account_id(get_token()), request.json)


@api.route('/<int:brand_id>')
@api.param('brand_id', 'A brand identifier associated with the authorized account.')
@api.response(brand_service.BrandServiceResponse.DoesNotExist, 'The requested brand does not exist.')
class BrandResource(Resource):
    @api.response(brand_service.BrandServiceResponse.Success, 'The brand was successfully deleted.')
    @api.response(brand_service.BrandServiceResponse.DoesNotExist, 'The requested brand does not exist.')
    @api.doc('Delete the brand.', security='jwt')
    @auth_required(api)
    def delete(self, brand_id):
        brand = brand_service.get_brand_by_id(get_account_id(get_token()), brand_id)

        if not brand:
            api.abort(brand_service.BrandServiceResponse.DoesNotExist)

        return brand_service.delete_brand(brand)

    @api.doc('Retrieve details about the brand.', security='jwt')
    @api.response(brand_service.BrandServiceResponse.DoesNotExist, 'The requested brand does not exist.')
    @auth_required(api)
    def get(self, brand_id):
        brand = brand_service.get_brand_by_id(get_account_id(get_token()), brand_id)

        if not brand:
            api.abort(brand_service.BrandServiceResponse.DoesNotExist)

        sentiment = get_brand_sentiment(brand)
        return {'id': brand.id, 'name': brand.name, 'average': sentiment['average'], 'trend': sentiment['trend']}

    @api.response(brand_service.BrandServiceResponse.Success, 'Brand details updated successfully.')
    @api.response(brand_service.BrandServiceResponse.AlreadyExists, 'The brand cannot be renamed to an existing brand.')
    @api.response(brand_service.BrandServiceResponse.DoesNotExist, 'The requested brand does not exist.')
    @api.doc('Update details about the brand.', security='jwt')
    @api.expect(BrandDTO.brand, validate=True)
    @auth_required(api)
    def put(self, brand_id):
        if not request.json['name'].strip():
            api.abort(400)

        brand = brand_service.get_brand_by_id(get_account_id(get_token()), brand_id)

        if not brand:
            api.abort(brand_service.BrandServiceResponse.DoesNotExist)

        return brand_service.update_brand_name(account_id=get_account_id(get_token()), brand=brand, change_data=request.json)


@api.route('/<int:brand_id>/synonyms')
@api.param('brand_id', 'A brand identifier associated with the authorized account.')
class BrandSynonymsResource(Resource):
    @api.response(brand_service.BrandServiceResponse.DoesNotExist, 'The requested brand does not exist.')
    @api.doc('Retrieve all synonyms associated with the brand.', security='jwt')
    @auth_required(api)
    def get(self, brand_id):
        brand = brand_service.get_brand_by_id(get_account_id(get_token()), brand_id)

        if not brand:
            api.abort(brand_service.BrandServiceResponse.DoesNotExist)

        synonyms = synonym_service.get_brand_synonyms(brand.id)

        # Instead of returning the model for each synonym, we just return the synonym itself
        return [{'synonym': synonym.synonym} for synonym in synonyms]

    @api.response(brand_service.BrandServiceResponse.DoesNotExist, 'The requested brand does not exist.')
    @api.expect(SynonymDTO.synonym, validate=True)
    @api.doc('Create a new synonym to be associated with the brand.', security='jwt')
    @auth_required(api)
    def post(self, brand_id):
        if not request.json['synonym'].strip():
            api.abort(400)

        brand = brand_service.get_brand_by_id(get_account_id(get_token()), brand_id)

        if not brand:
            api.abort(brand_service.BrandServiceResponse.DoesNotExist)

        return synonym_service.add_synonym(brand.id, request.json)


@api.route('/<int:brand_id>/synonyms/<string:synonym>')
class BrandSynonymResource(Resource):
    @api.response(brand_service.BrandServiceResponse.DoesNotExist, 'The requested brand does not exist.')
    @api.doc('Delete a synonym\'s association with a brand.', security='jwt')
    @auth_required(api)
    def delete(self, brand_id, synonym):
        brand = brand_service.get_brand_by_id(get_account_id(get_token()), brand_id)

        if not brand:
            api.abort(brand_service.BrandServiceResponse.DoesNotExist)

        return synonym_service.delete_synonym(brand_id, synonym)
