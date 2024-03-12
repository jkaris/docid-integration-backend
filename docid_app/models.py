from datetime import datetime

from .db import db


class AppUser(db.Model):
    __tablename__ = 'app_user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class DocIDObject(db.Model):
    __tablename__ = 'object_register'

    object_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    object_docid = db.Column(db.Integer, unique=True, nullable=False)
    object_category_id = db.Column(db.Integer, unique=True, nullable=False, foreign_key='objectcategory.object_id')
    object_title = db.Column(db.String(100), nullable=False)
    object_description = db.Column(db)
    user_id = db.Column(db.Integer, db.ForeignKey('appuser.user_id'))
    date_registered = db.Column(db.DateTime, default=datetime.utcnow)
    object_type_id = db.Column(db.Integer, db.ForeignKey('objecttype.object_type_id'))

class ObjectCategory(db.Model):
    __tablename__ = 'object_category'
    object_category_id = db.Column(db.Integer, pk=True, unique=True, nullable=False)
    object_category_name = db.Column(db.String(100), nullable=False)


class ObjectDataset(db.Model):
    __tablename__ = 'object_dataset'

    object_dataset_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    object_dataset_name = db.Column(db.String(100), nullable=False)
    datacite_doi = db.Column(db.String(100), nullable=False)
    object_title = db.Column(db.String(100), nullable=False)
    object_description = db.Column(db.String(100), nullable=False)
    docid_doi = db.Column(db.Integer, foreign_key='object_registration.object_docid', nullable=False)


class ObjectFile(db.Model):
    __tablename__ = 'object_file'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roa_doi = db.Column(db.Integer)
    file_title = db.Column(db.String(100), nullable=False)
    file_description = db.Column(db.String(100), nullable=False)
    docid_doi = db.Column(db.Integer, foreign_key='object_registration.object_docid', nullable=False)


class ObjectOrganization(db.Model):
    __tablename__ = 'object_organization'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organization_name = db.Column(db.String(100), nullable=False)
    organization_description = db.Column(db.String(100), nullable=False)
    ror_doi = db.Column(db.String(100), nullable=False)
    docid_doi = db.Column(db.Integer, foreign_key='object_registration.object_docid', nullable=False)


class PidLokup(db.Model):
    __tablename__ = 'pid_lookup'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    pid = db.Column(db.Text, nullable=False, unique=True)
    pid_reserved = db.Column(db.Integer)
    pid_reserved_date = db.Column(db.Text)
    pid_reserved_by = db.Column(db.Text)
    pid_assigned = db.Column(db.Integer)
    pid_assigned_date = db.Column(db.Text)
    pid_assigned_by = db.Column(db.Text)
    docid_doi = db.Column(db.Integer, foreign_key='object_registration.object_docid', nullable=False)


class Language(db.Model):
    __tablename__ = 'language'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)


def init_db():
    """Create database tables."""
    db.create_all()
