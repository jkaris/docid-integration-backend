from flask import Blueprint, request, jsonify
from .models import PublicationFormData

bp = Blueprint("utils", __name__, url_prefix="/utils")


@bp.route('/get-publications/all', methods=['GET'])
def get_all_publications():
    try:
        data = PublicationFormData.query.all()
        if len(data) == 0:
            return jsonify({'message': 'No matching records found'}), 404
        data_list = [{'id': item.id, 'data': item.form_data} for item in data]
        return jsonify(data_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/get-publication/<int:publication_id>', methods=['GET'])
def get_publication(publication_id):
    try:
        data = PublicationFormData.query.get(publication_id)
        if not data:
            return jsonify({'message': 'No matching records found'}), 404
        return jsonify({'id': data.id, 'data': data.form_data})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/get-publications/<title>', methods=['GET'])
def get_publications_title(title):
    try:
        data = PublicationFormData.query.filter(PublicationFormData.form_data.op('->>')('title').like(f"%{title}%")).all()
        if len(data) == 0:
            return jsonify({'message': 'No matching records found'}), 404
        data_list = [{'id': item.id, 'data': item.form_data} for item in data]
        return jsonify(data_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
