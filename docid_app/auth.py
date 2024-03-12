import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    print(data)
    db = get_db()
    error = None

    if not data.get('firstName'):
        error = 'First name is required.'
    elif not data.get('lastName'):
        error = 'Last name is required.'
    elif not data.get('email'):
        error = 'Email is required.'
    elif not data.get('password'):
        error = 'Password is required.'
    elif db.execute(
        'SELECT user_id FROM appuser WHERE email = ?', (data['email'],)
    ).fetchone() is not None:
        error = f'User already registered.'

    if error is None:
        db.execute(
            'INSERT INTO appuser (first_name, last_name, email, password) VALUES (?, ?, ?, ?)',
            (data['firstName'], data['lastName'], data['email'], generate_password_hash(data['password']))
        )
        db.commit()
        return jsonify({'message': 'Registration successful'})

    return jsonify({'message': error}), 400

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    db = get_db()
    error = None
    user = db.execute(
        'SELECT * FROM appuser WHERE email = ?', (data['email'],)
    ).fetchone()

    if user is None or not check_password_hash(user['password'], data['password']):
        error = 'Incorrect password.'

    if error is None:
        session.clear()
        session['user_id'] = user['user_id']
        return jsonify({'message': 'Login successful'})

    return jsonify({'error': error}), 401

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM appuser WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful'})

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view