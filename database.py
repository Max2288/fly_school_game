"""A file for interacting with the database."""

import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from os import getenv
from dotenv import load_dotenv
from config import *
from werkzeug.security import generate_password_hash, check_password_hash
from logger import init_logger


load_dotenv()
init_logger('database')
logger = logging.getLogger("database")


def create_pg_connection():
    """Create connection.

    Returns:
        conenction: connection to db.
    """
    conn = psycopg2.connect(
        host=getenv('DB_HOST'),
        port=getenv('DB_PORT'),
        database=getenv('DATABASE'),
        user=getenv('DB_USER'),
        password=getenv('DB_PASSWORD'),
        cursor_factory=RealDictCursor,
    )
    conn.autocommit = True
    return conn


def register_in_db(users_dict: dict):
    """Register user in database.

    Args:
        users_dict (dict): dictionary with user data.

    Returns:
        list: data to request.
    """
    username = users_dict['username']
    try:
        with create_pg_connection() as conn, conn.cursor() as cur:
            cur.execute(CHECK_QUERY, (username,))
            if cur.fetchone():
                return 'This username is already taken!', ISUSED
            cur.execute(REGISTER_QUERY, (username, generate_password_hash(users_dict['password'])))
            logger.info(f"User with username {username} created successfully")
            return 'User created successfully', CREATED
    except Exception as ex:
        logger.error(ex, exc_info=True)
        return '', BADREQV


def check_auth(users_dict: dict):
    """Check user information, then authentificate.

    Args:
        users_dict (dict): dictionary with user data.

    Returns:
        list: data to request.
    """
    username = users_dict['username']
    try:
        with create_pg_connection() as conn, conn.cursor() as cur:
            cur.execute(CHECK_QUERY, (username,))
            if not cur.fetchone():
                return 'There is not users with this username!', NOT_FOUND
            cur.execute(AUTH_QUERY, (username,))
            data_from_db = cur.fetchall()[0]
            if check_password_hash(data_from_db['password'], users_dict['password']):
                logger.info(f"User with username {username} logined successfully")
                list_to_join = [username] + [str(values_from_db) for _, values_from_db in data_from_db.items()][1:]
                return ' '.join(list_to_join), OK
            return 'Wrong password!', FORBIDDEN
    except Exception as ex:
        logger.error(ex, exc_info=True)
        return '', BADREQV


def update_db(users_dict: dict):
    """Update user info in db.

    Args:
        users_dict (dict): dictionary with user data.

    Returns:
        list: data to request.
    """
    username = users_dict['username']
    try:
        with create_pg_connection() as conn, conn.cursor() as cur:
            cur.execute(
                UPDATE_QUERY % (users_dict['x'], users_dict['y']) +
                ' WHERE username = (%s) RETURNING id', (username, ),
            )
            data_from_db = cur.fetchone()
            if data_from_db:
                logger.info(f"User with username {username} left game, data was updated")
                return '', UPDATED
            return 'No data updated!', BADREQV
    except Exception as ex:
        logger.error(ex, exc_info=True)
        return '', BADREQV
