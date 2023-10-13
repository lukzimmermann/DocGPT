from flask import Blueprint, request
import bcrypt
import postgres

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login():
    data = request.json

    username = data.get('mailAddress')
    password = data.get('password')

    pg = postgres.PostgresDB()
    pg.connect()

    data = (username,)
    response = pg.selectQuery("""
                   SELECT *
                   FROM users
                   WHERE email = %s
                   """, data)

    pg.disconnect()

    if bcrypt.checkpw(password.encode('utf-8'), response[0][2].encode('utf-8')):
        return 'Login page'
    else:
        return 'wrong username or password'


@auth_bp.route('/create')
def create():
    data = request.json

    username = data.get('mailAddress')
    password = data.get('password')

    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(password.encode('utf-8'), salt)

    pg = postgres.PostgresDB()
    pg.connect()

    data = (username, hashedPassword)

    pg.executeQuery("""
                    INSERT INTO users
                    (email, password_hash)
                    VALUES (%s, %s)
                    """, data)

    pg.disconnect()

    return 'Logout page'


@auth_bp.route('/logout')
def logout():
    return 'Logout page'
