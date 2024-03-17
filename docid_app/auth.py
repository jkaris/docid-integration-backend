import functools

from flask import Blueprint, g, redirect, request, session, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from .models import UserAccount
from .db import db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["POST"])
def register():
    data = request.json
    error = None
    user_name = data.get("userName")
    user_full_name = data.get("userFullName")
    user_affiliations = data.get("userAffiliations")
    user_email = data.get("userEmail")
    user_password = data.get("userPassword")
    existing_user = UserAccount.query.filter(
        (UserAccount.email == user_email) | (UserAccount.user_name == user_name)
    ).first()
    if existing_user:
        error = "User already exists"
        return jsonify({"message": error}), 400
    hashed_password = generate_password_hash(user_password)
    new_user = UserAccount(
        user_name=user_name,
        full_name=user_full_name,
        affiliation=user_affiliations,
        email=user_email,
        password=hashed_password,
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Registration successful"})


@bp.route("/login", methods=["POST"])
def login():
    data = request.json
    error = None
    user_email = data.get("userEmail")
    user_password = data.get("userPassword")
    user = UserAccount.query.filter(UserAccount.email == user_email).first()

    if user and check_password_hash(user.password, user_password):
        session["user_id"] = user.user_id
        return jsonify({"message": "Login successful"})
    else:
        error = "Invalid username/email or password."
        return jsonify({"message": error}), 401


@bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "You have been logged successful"})


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
