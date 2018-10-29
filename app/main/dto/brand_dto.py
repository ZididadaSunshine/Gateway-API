from flask_restplus import fields, Namespace


class BrandDTO:
    api = Namespace('Brand', description='Brand operations.')
    new_brand = api.model('Brand details', {
        'name': fields.String(required=True, description='Name of the brand.'),
    })
