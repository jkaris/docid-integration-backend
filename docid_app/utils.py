# from flask import (
#     Blueprint, request, jsonify, g
# )
#
# from .db import db
#
# from .models import ObjectCategory
#
# bp = Blueprint('utils', __name__, url_prefix='/utils')
#
# @bp.route('/object-types', methods=['GET'])
# def get_resource_types():
#     try:
#         object_types = db.session.query(ObjectCategory).all()
#         return jsonify(object_types)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#
# @bp.route('/get-publications', methods=['GET'])
# def get_publications():
#     try:
#         db = get_db()
#         publications = db.execute("SELECT bi.*, fr.file_name, fr.file_path FROM basic_information bi JOIN file_record fr ON bi.file_id=fr.id").fetchall()
#         publications_json = [{'id': row["id"], 'title': row["title"], 'doi': row['doi'], 'file_name': row['file_name']} for row in publications]
#         return jsonify(publications_json)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#
# from flask import request
#
# @bp.route('/get-publication/<int:publication_id>', methods=['GET'])
# def get_publication(publication_id):
#     try:
#         db = get_db()
#         publication = db.execute("SELECT bi.*, fr.file_name, fr.file_path FROM basic_information bi JOIN file_record fr ON bi.file_id=fr.id WHERE bi.id = ?", (publication_id,)).fetchone()
#         if publication:
#             publication_json = {
#                 'id': publication["id"],
#                 'title': publication["title"],
#                 'doi': publication['doi'],
#                 'file_name': publication['file_name']
#             }
#             return jsonify(publication_json)
#         else:
#             return jsonify({'error': 'Publication not found'}), 404
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#
#
# @bp.route('/get-publications/<title>', methods=['GET'])
# def get_publications_title(title):
#     try:
#         publication = f"%{title}%"
#         db = get_db()
#         publications = db.execute("SELECT * FROM basic_information WHERE LOWER(title) LIKE ? LIMIT 10", (publication,)).fetchall()
#         publications_json = [{'id': row["id"], 'title': row["title"]} for row in publications]
#         return jsonify(publications_json)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
