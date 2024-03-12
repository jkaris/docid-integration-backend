import functools

from flask import (
    Blueprint, g, redirect, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from .models import AppUser
from .db import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    error = None
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')
    password = data.get('password')

    # Check if the username or email already exists
    existing_email = AppUser.query.filter_by(email=email).first()
    if existing_email:
        error = 'User already exists'
        return jsonify({'message': error}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create a new user object
    new_user = AppUser(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registration successful'})


@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    error = None
    email = data.get('email')
    password = data.get('password')
    user = AppUser.query.filter(AppUser.email == email).first()

    if user and check_password_hash(user.password, password):
        session['user_id'] = user.user_id
        return jsonify({'message': 'Login successful'})
    else:
        error = 'Invalid username/email or password.'
        return jsonify({'message': error}), 401


@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'You have been logged successful'})


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
