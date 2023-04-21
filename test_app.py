"""Testing file."""

from fastapi.testclient import TestClient
from main import app
from config import *
import psycopg2
from psycopg2.extras import RealDictCursor
from os import getenv
from dotenv import load_dotenv


client = TestClient(app)
load_dotenv()


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


def test_setup():
    """Create tables for tests."""
    with create_pg_connection() as conn, conn.cursor() as cur:
        with open('init_db.ddl', 'r') as init_db:
            cur.execute(init_db.read())


def test_rec():
    """Test for reciving data."""
    data_from_user = {"time": "2023-04-21T12:00:00Z", "key_pressed": "a", "x": 0, "y": 0}
    response = client.post("/rec", json=data_from_user)
    assert response.status_code == CREATED
    assert response.text == "Data recieved"


def test_register():
    """Test for registration."""
    user = {"username": "test1", "password": "testpass1"}
    response = client.post("/register", json=user)
    assert response.status_code == CREATED
    assert response.text == "User created successfully"


def test_auth():
    """Test for authentification."""
    user = {"username": "test1", "password": "testpass1"}
    response = client.post("/auth", json=user)
    assert response.status_code == OK
    assert response.text == "test1 0 0"


def test_update():
    """Test for updating user data."""
    user = {"username": "test1", "x": 10, "y": 20}
    response = client.put("/update", json=user)
    assert response.status_code == UPDATED
