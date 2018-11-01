import datetime

from app.main import db
from app.main.model.brand_synonym_association import BrandSynonym
from app.main.model.synonym_model import Synonym


class SynonymServiceResponse:
    Success = 200
    Created = 201
    AlreadyExists = 400
    DoesNotExist = 404


def get_synonyms(brand_id):
    """ Get the synonyms associated with a brand. """
    return Synonym.query.join(BrandSynonym, (Synonym.id == BrandSynonym.synonym_id) & (BrandSynonym.brand_id == brand_id)).all()


def add_synonym(brand_id, synonym_data):
    """ Add a synonym to be associate with a brand. """
    synonym = synonym_data['synonym']

    # Check if the synonym already exists
    # If it does not exist, create it
    existing = Synonym.query.filter(Synonym.synonym.ilike(synonym)).first()
    if not existing:
        synonym = Synonym(synonym=synonym)

        db.session.add(synonym)
        db.session.flush()  # Needed to get the new id, though the row is not visible to other transactions

        # Refresh the current session in order to get the new synonym
        db.session.refresh(synonym)
        existing = synonym

    # Check if the synonym is already associated with the brand
    if BrandSynonym.query.filter((BrandSynonym.brand_id == brand_id) & (BrandSynonym.synonym_id == existing.id)).scalar():
        return dict(success=False,
                    message="The synonym is already associated with the brand."), SynonymServiceResponse.AlreadyExists

    # Create an association between the synonym and the brand
    association = BrandSynonym(brand_id=brand_id, synonym_id=existing.id, created_at=datetime.datetime.utcnow())

    db.session.add(association)
    db.session.commit()

    return dict(success=True), SynonymServiceResponse.Created


def delete_synonym(brand_id, synonym):
    # Get the associated synonym
    existing = Synonym.query.filter_by(synonym=synonym).\
        join(BrandSynonym, (BrandSynonym.brand_id == brand_id) & (BrandSynonym.synonym_id == Synonym.id)).first()
    if not existing:
        return dict(success=False, message='The requested synonym does not exist.'), SynonymServiceResponse.DoesNotExist

    # Delete the association
    BrandSynonym.query.filter_by(synonym_id=existing.id).delete()
    db.session.commit()

    # Currently, we do not care about deleting orphaned synonyms
    # TODO: Might want to delete orphaned synonyms without mentions in the future

    return dict(success=True), SynonymServiceResponse.Success
