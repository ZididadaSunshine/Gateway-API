from flask_restplus import fields, Namespace


class SynonymDTO:
    api = Namespace('Synonym', description='Synonym operations that are brand agnostic.')

    synonym = api.model('Synonym details', {
        'synonym': fields.String(required=True, description='A synonym string.')
    })
