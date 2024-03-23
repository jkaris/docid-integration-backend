from .models import (
    DocIdLookup,
)

from .db import db
from datetime import datetime


def insert_data():
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
