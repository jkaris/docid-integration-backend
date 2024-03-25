import os
import sqlite3
from flask import Blueprint, request, jsonify, current_app, g
from datetime import datetime
from .models import PublicationFormData

from .db import db

# from tccapp.db import get_db

bp = Blueprint("save", __name__, url_prefix="/save")


def save_file_info(file_name, file_path, file_extension, upload_date):
    mydb = sqlite3.connect(
        current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
    )
    cursor = mydb.cursor()
    cursor.execute(
        """
        INSERT INTO file_record (file_name, file_path, file_extension, upload_date)
        VALUES (?, ?, ?, ?)
    """,
        (file_name, file_path, file_extension, upload_date),
    )
    mydb.commit()
    last_id = cursor.lastrowid
    return last_id


def save_basic_info(
    title,
    pub_date,
    doi,
    resource_type_id,
    description,
    family_name,
    given_name,
    identifier,
    affiliation,
    role,
    file_id,
):
    """
    Save record into the database.
    """
    db = g.get_db()
    db.execute(
        """
        INSERT INTO basic_information (title, pub_date, doi,
        resource_type_id, description, family_name, given_name, identifier, affiliation, role,file_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            pub_date,
            doi,
            resource_type_id,
            description,
            family_name,
            given_name,
            identifier,
            affiliation,
            role,
            file_id,
        ),
    )
    db.commit()
    db.close()


@bp.route("/file-info", methods=["POST"])
def save_file_record():
    files = request.files

    print(len(files))

    for file in files.getlist('files'):  # Assuming key is 'file'
        filename = file.filename  #
        file_type = file.content_type
        print(f"filename: {filename}, file_type: {file_type}")
        # ess filename here
    print("Hi there")
    # try:
    #     if "file" not in request.files:
    #         return jsonify({"error": "No file part"}), 400
    #
    #     file = request.files["file"]
    #     if file.filename == "":
    #         return jsonify({"error": "No selected file"}), 400
    #
    #     project_dir = os.path.dirname(os.path.abspath(__file__))
    #     uploads_dir = os.path.join(project_dir, "uploads")
    #     # Create the uploads directory if it doesn't exist
    #     if not os.path.exists(uploads_dir):
    #         os.makedirs(uploads_dir)
    #
    #     file_name = file.filename
    #     file_path = os.path.join(uploads_dir, file_name)
    #     file_extension = os.path.splitext(file_name)[1]
    #     upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #
    #     # Save the file to a desired location
    #     file.save(file_path)
    #
    #     _id = save_file_info(file_name, file_path, file_extension, upload_date)

    return jsonify({"message": "File uploaded successfully"})
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500


# @bp.route("/basic-info", methods=["POST"])
# def save_basic_info_record():
#     """
#     Save basic information to database.
#     """
#     try:
#         data = request.json
#         title = data["title"]
#         pub_date = data["selectedDate"]
#         doi = data["doi"]
#         resource_type_id = data["selectedResourceType"]
#         description = data["description"]
#         family_name = data["familyName"]
#         given_name = data["givenName"]
#         identifier = data["identifiers"]
#         affiliation = data["affiliations"]
#         role = data["roles"]
#         file_id = data["fileId"]
#
#         save_basic_info(
#             title,
#             pub_date,
#             doi,
#             resource_type_id,
#             description,
#             family_name,
#             given_name,
#             identifier,
#             affiliation,
#             role,
#             file_id,
#         )
#
#         return jsonify({"message": "Form data saved successfully"}), 200
#     except Exception as e:
#         # db.session.rollback()
#         return jsonify({"error": str(e)}), 500


@bp.route("/publish", methods=["POST"])
def publish_record():
    """
    Save basic information to database.
    """
    try:
        data = request.json
        form_data = data["formData"]
        user_id = data["publisher"]

        publication = PublicationFormData(
            form_data=form_data,
            user_id=user_id
        )
        db.session.add(publication)
        db.session.commit()

        # print(form_data)

        # publish_record(
        #     form_data,
        #     user_id
        # )

        return jsonify({"message": "Form data saved successfully"}), 200
    except Exception as e:
        # db.session.rollback()
        return jsonify({"error": str(e)}), 500
