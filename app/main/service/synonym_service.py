from app.main import db
from app.main.model.synonym_model import Synonym


class SynonymServiceResponse:
    Success = 200
    Created = 201
    BrandHasSynonym = 400


def get_synonyms(brand_id):
    """ Get the synonyms associated with a brand. """
    pass


def add_synonym(brand_id, data):
    """ Add a synonym to be associate with a brand. """
    synonym = data['synonym']

    # Check if the synonym already exists
    existing = Synonym.query.filter_by(identifier=synonym)
    if not existing:
        synonym = Synonym(identifier=synonym)

        db.session.add(synonym)
        db.session.commit()

        # Refresh the current session in order to get the id of the new synonym
        db.session.refresh()
        existing = synonym

        print(existing.id)
