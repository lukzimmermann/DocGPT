from flask import Blueprint, request, jsonify
import bcrypt
import psycopg2
import postgres

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('email')
    password = data.get('password')

    pg = postgres.PostgresDB()
    pg.connect()

    data = (username,)
    response = pg.selectQuery("""
                   SELECT pass
                   FROM users
                   WHERE email = %s
                   """, data)
    pg.disconnect()

    if response and len(response) == 1:
        stored_hash = response[0][0]
        hash = bcrypt.hashpw(password.encode('utf-8'), stored_hash.encode('utf-8'))

        if hash.decode('utf-8') == stored_hash:
            response_message = {
                "message": "Login successful."
                }
            return jsonify(response_message), 200
    

    response_message = {"message": "Wrong username or password"}
    return jsonify(response_message), 401



@auth_bp.route('/create')
def create():
    data = request.json

    email = data.get('email')
    password = data.get('password')

    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(password.encode('utf-8'), salt)

    pg = postgres.PostgresDB()
    pg.connect()

    data = (email, hashedPassword.decode('utf-8'))

    pg.executeQuery("""
                    INSERT INTO users
                    (email, pass)
                    VALUES (%s, %s)
                    """, data)

    pg.disconnect()

    return 'Create'


@auth_bp.route('/logout')
def logout():
    return 'Logout page'
