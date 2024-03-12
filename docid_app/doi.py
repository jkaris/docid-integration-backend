import random
import requests
from flask import (
    Blueprint, request, jsonify,
)
from tccapp.db import get_db

bp = Blueprint('doi', __name__, url_prefix='/doi')

@bp.route("/get-datacite-doi", methods=["GET"])
def get_datacite_doi():
    try:
        url = "https://api.test.datacite.org/dois?client_id=datacite.datacite"
        headers = {
            "Content-Type": "application/json"
        }
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


@bp.route('/get-docid-doi', methods=['GET'])
def get_docid():
    """
    Get Doc ID from PID log table.
    """
    try:
        db = get_db()
        random_datacite_pid = db.execute(
            "SELECT pid FROM pid_log ORDER BY RANDOM() LIMIT 1"
        ).fetchone()
        if random_datacite_pid:
            return jsonify({'docid_doi': random_datacite_pid['pid'][:7]})
        else:
            return jsonify({'error': 'No random datacite DOI found'})

    except Exception as e:
        return jsonify({'error': 'Failed to fetch datacite DOI: ' + str(e)})
