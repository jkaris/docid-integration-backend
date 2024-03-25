import requests
from flask import (
    Blueprint,
    jsonify,
)
from sqlalchemy.sql import func
from .db import db
from .models import DocIdLookup

bp = Blueprint("doi", __name__, url_prefix="/doi")


@bp.route("/get-datacite-doi", methods=["GET"])
def get_datacite_doi():
    """
        Get DataCite DOI from DataCite API.
    """
    try:
        url = (
            "https://api.test.datacite.org/dois?client_id=datacite.datacite&random=true"
        )
        headers = {"Content-Type": "application/json"}
        repository_id, password = "FPAV", "Tremis#123$"
        response = requests.get(
            url=url,
            headers=headers,
            auth=(repository_id, password),
        )
        response.raise_for_status()
        data = response.json()
        doi = data["data"][0]["id"]

        return jsonify({"doi": doi})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch datacite DOI: {str(e)}"}), 500


@bp.route("/get-docid-doi", methods=["GET"])
def get_docid():
    """
    Get Doc ID from PID log table.
    """
    try:
        random_docid_pid = (
            db.session.query(DocIdLookup).order_by(func.random()).first()
        )
        return jsonify({"docid_doi": random_docid_pid.pid[:7]})
        # else:
        #     return jsonify({"error": "No random DocID DOI found"})
    except Exception as e:
        return jsonify({"error": "Failed to fetch DocID DOI: " + str(e)})
