from .models import (
    Language,
    ObjectCategory,
    ObjectDataSetType,
    UserAccount,
    DocIdLookup,
)

from .db import db
from datetime import datetime

# DEFAULT_USER = AppUser(first_name="Default", last_name="User", affiliation="No affiliation", date_joined=datetime.utcnow(),
#             email="default@email.com", password="somepassword123_")

LANGUAGES = [
    Language(name="English", short_name="en", description="English language"),
    Language(name="Swahili", short_name="sw", description="Swahili language"),
    Language(name="Portuguese", short_name="pt", description="Portuguese language"),
]

OBJECT_CATEGORIES = [
    ObjectCategory(
        object_category_name="Indigenous Knowledge",
        object_category_description="indigenous knowledge",
    ),
    ObjectCategory(object_category_name="Patent", object_category_description="patent"),
    ObjectCategory(
        object_category_name="Cultural Heritage",
        object_category_description="cultural heritage",
    ),
    ObjectCategory(
        object_category_name="Project", object_category_description="project"
    ),
    ObjectCategory(object_category_name="Funder", object_category_description="funder"),
    ObjectCategory(
        object_category_name="Article", object_category_description="article"
    ),
    ObjectCategory(
        object_category_name="Dataset", object_category_description="dataset"
    ),
]


DATASET_TYPES = [
    ObjectDataSetType(
        object_dataset_type_name="Video",
        object_dataset_type_description="video dataset",
    ),
    ObjectDataSetType(
        object_dataset_type_name="Webinar",
        object_dataset_type_description="webinar dataset",
    ),
    ObjectDataSetType(
        object_dataset_type_name="Illustration",
        object_dataset_type_description="illustration dataset",
    ),
    ObjectDataSetType(
        object_dataset_type_name="Interview",
        object_dataset_type_description="interview dataset",
    ),
    ObjectDataSetType(
        object_dataset_type_name="Conference Proceeding",
        object_dataset_type_description="conference proceeding dataset",
    ),
]


def insert_data():
    existing_languages = [
        record.name
        for record in db.session.query(Language)
        .filter(Language.name.in_(record.name for record in LANGUAGES))
        .all()
    ]
    languages_to_insert = [
        record for record in LANGUAGES if record.name not in existing_languages
    ]

    existing_obj_categories = [
        record.object_category_name
        for record in db.session.query(ObjectCategory)
        .filter(
            ObjectCategory.object_category_name.in_(
                record.object_category_name for record in OBJECT_CATEGORIES
            )
        )
        .all()
    ]
    obj_categories_to_insert = [
        record
        for record in OBJECT_CATEGORIES
        if record.object_category_name not in existing_obj_categories
    ]
    db.session.add_all(languages_to_insert)
    # db.session.add(DEFAULT_USER)
    db.session.add_all(obj_categories_to_insert)
    # db.session.add_all(DATASET_TYPES)
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
        # pid_reserved_by = 1
        pid_assigned = False
        pid_assigned_date = datetime.utcnow()
        # pid_assigned_by = 1
        # docid_doi = None
        # Create an instance of the model with the field values
        record = DocIdLookup(
            name=name,
            description=description,
            pid=pid,
            pid_reserved=pid_reserved,
            pid_reserved_date=pid_reserved_date,
            # pid_reserved_by=pid_reserved_by,
            pid_assigned=pid_assigned,
            pid_assigned_date=pid_assigned_date,
            # pid_assigned_by=pid_assigned_by,
            # docid_doi=docid_doi
        )
        records.append(record)
    existing_records = [
        record.pid
        for record in db.session.query(DocIdLookup)
        .filter(DocIdLookup.pid.in_(record.pid for record in records))
        .all()
    ]
    records_to_insert = [
        record for record in records if record.pid not in existing_records
    ]

    # Add all records to the session
    db.session.add_all(records_to_insert)

    # Commit the changes to the database
    db.session.commit()
    db.session.close()
