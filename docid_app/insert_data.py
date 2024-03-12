from .models import (
    Language,
    ObjectCategory,
    ObjectDataSetType,
    AppUser,
    DocIdLookup,
)

from .db import db
from datetime import datetime

DEFAULT_USER = AppUser(first_name="Default", last_name="User", affiliation="No affiliation", date_joined=datetime.utcnow(),
            email="default@email.com", password="somepassword123_")

LANGUAGES = [
    Language(name='English', short_name="en", description="English language"),
    Language(name='Swahili', short_name="sw", description="Swahili language"),
    Language(name='Portuguese', short_name="pt", description="Portuguese language")
]

OBJECT_CATEGORIES = [
    ObjectCategory(object_category_name='Indigenous Knowledge', object_category_description='indigenous knowledge'),
    ObjectCategory(object_category_name='Patent', object_category_description='patent'),
    ObjectCategory(object_category_name='Cultural Heritage', object_category_description='cultural heritage'),
    ObjectCategory(object_category_name='Project', object_category_description='project'),
    ObjectCategory(object_category_name='Funder', object_category_description='funder'),
    ObjectCategory(object_category_name='Article', object_category_description='article'),
    ObjectCategory(object_category_name='Dataset', object_category_description='dataset')

]

DATASET_TYPES = [
    ObjectDataSetType(object_dataset_type_name='Video', object_dataset_type_description='video dataset'),
    ObjectDataSetType(object_dataset_type_name='Webinar', object_dataset_type_description='webinar dataset'),
    ObjectDataSetType(object_dataset_type_name='Illustration', object_dataset_type_description='illustration dataset'),
    ObjectDataSetType(object_dataset_type_name='Interview', object_dataset_type_description='interview dataset'),
    ObjectDataSetType(object_dataset_type_name='Conference Proceeding',
                      object_dataset_type_description='conference proceeding dataset'),
]


def insert_data():
    db.session.add(DEFAULT_USER)
    db.session.add_all(LANGUAGES)
    db.session.add_all(OBJECT_CATEGORIES)
    db.session.add_all(DATASET_TYPES)
    db.session.commit()
    db.session.close()


def generate_pids():
    # Generate the series of numbers from 1 to 100
    series = range(1, 101)

    # Create a list to hold the records to be added to the session
    records = []

    # Iterate over the series and create instances of the model for each record
    for n in series:
        name = f"DOCID PID {n:04d}"
        description = "DOCID Sample DOI"
        pid = f"20.{n:04d}/{n:04d}"
        pid_reserved = False
        pid_reserved_date = datetime.utcnow()
        pid_reserved_by = 1
        pid_assigned = False
        pid_assigned_date = datetime.utcnow()
        pid_assigned_by = 1
        docid_doi = None
        # Create an instance of the model with the field values
        record = DocIdLookup(
            name=name,
            description=description,
            pid=pid,
            pid_reserved=pid_reserved,
            pid_reserved_date=pid_reserved_date,
            pid_reserved_by=pid_reserved_by,
            pid_assigned=pid_assigned,
            pid_assigned_date=pid_assigned_date,
            pid_assigned_by=pid_assigned_by,
            docid_doi=docid_doi
        )
        records.append(record)

    # Add all records to the session
    db.session.add_all(records)

    # Commit the changes to the database
    db.session.commit()
    db.session.close()
