"""Cinfig file for fly game."""

CHECK_QUERY = 'SELECT id from users where username=(%s)'
REGISTER_QUERY = 'INSERT into users(username, password) VALUES (%s, %s)'
AUTH_QUERY = 'SELECT password, x, y from users WHERE username = (%s)'
UPDATE_QUERY = 'UPDATE users SET (x,y) = (%d, %d)'

REGISTER_URL = 'http://127.0.0.1:8000/register'
AUTH_URL = 'http://127.0.0.1:8000/auth'
UPDATE_URL = 'http://127.0.0.1:8000/update'
MAIN_URL = 'http://127.0.0.1:8000/rec'

CREATED = 201

ISUSED = 226

BADREQV = 400

OK = 200

NOT_FOUND = 404

FORBIDDEN = 403

UPDATED = 204
