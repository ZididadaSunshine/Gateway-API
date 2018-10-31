from flask_restplus import fields, Namespace


class BrandDTO:
    api = Namespace('Brand', description='Brand operations.')

    brand = api.model('Brand details', {
        'id': fields.Integer(description='Internal identifier for the brand.'),
        'name': fields.String(required=True, description='Name of the brand.'),
    })

    synonym = api.model('Synonym details', {
        'identifier': fields.String(required=True,
                                    description='The identifier for the synonym, i.e. the synonym itself.')
    })
