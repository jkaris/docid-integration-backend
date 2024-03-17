from datetime import datetime

from .db import db


class UserAccount(db.Model):
    """
    User account
    """
    __tablename__ = 'user_account'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    # github_id = db.Column(db.String(100), nullable=False)
    # orcid_id = db.Column(db.String(100), nullable=False)
    # openaire_id = db.Column(db.String(100), nullable=False)
    affiliation = db.Column(db.String(100), nullable=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


# class DocIDObject(db.Model):
#     """
#     DocID Object
#     """
#     __tablename__ = 'docid_object'
#
#     object_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     object_docid = db.Column(db.Integer, unique=True, nullable=False)
#     object_category_id = db.Column(db.Integer, db.ForeignKey('object_category.object_category_id'))
#     object_title = db.Column(db.String(100), nullable=False)
#     object_description = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id'))
#     date_registered = db.Column(db.DateTime, default=datetime.utcnow)
#     object_type_id = db.Column(db.Integer, db.ForeignKey('object_category.object_category_id'))
#
#
class ObjectCategory(db.Model):
    __tablename__ = 'object_category'
    object_category_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    object_category_name = db.Column(db.String(100), nullable=False)
    object_category_description = db.Column(db.String(100), nullable=False)


# class ObjectDataset(db.Model):
#     """
#     Object dataset
#     """
#     __tablename__ = 'object_dataset'
#
#     object_dataset_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
#     object_dataset_name = db.Column(db.String(100), nullable=False)
#     object_dataset_description = db.Column(db.String(100), nullable=False)
#     datacite_doi = db.Column(db.String(100), nullable=False)
#     object_dataset_title = db.Column(db.String(100), nullable=False)
#     docid_doi = db.Column(db.Integer, db.ForeignKey('docid_object.object_docid'))
#     object_dataset_type = db.Column(db.Integer, db.ForeignKey('object_dataset_type.object_dataset_type_id'))
#
#
# class ObjectDataSetType(db.Model):
#     """
#     Object dataset types lookup table
#     """
#     __tablename__ = 'object_dataset_type'
#
#     object_dataset_type_id = db.Column(db.Integer, primary_key=True)
#     object_dataset_type_name = db.Column(db.String(100), nullable=False)
#     object_dataset_type_description = db.Column(db.String(100), nullable=False)
#
#
# class ObjectFile(db.Model):
#     """
#     Object file
#     """
#     __tablename__ = 'object_file'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     roa_doi = db.Column(db.Integer)
#     file_title = db.Column(db.String(100), nullable=False)
#     file_description = db.Column(db.String(100), nullable=False)
#     docid_doi = db.Column(db.Integer, db.ForeignKey('docid_object.object_docid'))
#
#
# class ObjectOrganization(db.Model):
#     """
#     Object organization
#     """
#     __tablename__ = 'object_organization'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     organization_name = db.Column(db.String(100), nullable=False)
#     organization_full_name = db.Column(db.String(100), nullable=False)
#     person_affiliations = db.Column(db.String(100), nullable=False)
#     person_role = db.Column(db.String(100), nullable=False)
#     ror_doi = db.Column(db.String(100), nullable=False)
#     docid_doi = db.Column(db.Integer, db.ForeignKey('docid_object.object_docid'))
#
#
# class ObjectIndividual(db.Model):
#     """
#     Object individual
#     """
#     __tablename__ = 'object_individual'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     person_name = db.Column(db.String(100), nullable=False)
#     person_family_name = db.Column(db.String(100), nullable=False)
#     person_given_names = db.Column(db.String(100), nullable=False)
#     person_affiliations = db.Column(db.String(100), nullable=False)
#     person_role = db.Column(db.String(100), nullable=False)
#     orcid_doi = db.Column(db.String(100), nullable=False)
#     docid_doi = db.Column(db.Integer, db.ForeignKey('docid_object.object_docid'))
#
#
class DocIdLookup(db.Model):
    """
    DocId lookup
    """
    __tablename__ = 'pid_lookup'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    pid = db.Column(db.Text, nullable=False, unique=True)
    pid_reserved = db.Column(db.Boolean, nullable=False, default=False)
    pid_reserved_date = db.Column(db.DateTime, default=datetime.utcnow)
    # pid_reserved_by = db.Column(db.Integer, db.ForeignKey('app_user.user_id'))
    pid_assigned = db.Column(db.Boolean, nullable=False, default=False)
    pid_assigned_date = db.Column(db.DateTime, default=datetime.utcnow)
    # pid_assigned_by = db.Column(db.Integer, db.ForeignKey('app_user.user_id'))
    # docid_doi = db.Column(db.Integer, db.ForeignKey('docid_object.object_docid'))


class Language(db.Model):
    """
    Language lookup
    """
    __tablename__ = 'language'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    short_name = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)


def init_db():
    """Create database tables."""
    db.create_all()
