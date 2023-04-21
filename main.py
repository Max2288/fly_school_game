"""File for fastapi server."""
from fastapi import FastAPI, Response
from jinja2 import Environment, FileSystemLoader
from config import *
import uvicorn
from database import register_in_db, check_auth, update_db
from pydantic import BaseModel
import logging


class User(BaseModel):
    """User model."""

    username: str
    password: str

    def to_dict(self):
        """Create fict from class.

        Returns:
            dcit: user's dict
        """
        return self.__dict__


class UserInGame(BaseModel):
    """User in game model."""

    username: str
    x: int
    y: int

    def to_dict(self):
        """Create fict from class.

        Returns:
            dcit: user's dict
        """
        return self.__dict__


class UserData(BaseModel):
    """User data model."""

    time: str
    key_pressed: str
    x: int
    y: int


app = FastAPI()
env = Environment(loader=FileSystemLoader('templates'), autoescape=True)
logger = logging.getLogger("database")


@app.post("/rec")
async def root(data_from_user: UserData) -> Response:
    """Recieve telemetry from game.

    Args:
        data_from_user (UserData): dict with user telemetry.

    Returns:
        Response: request response.
    """
    logger.info(data_from_user)
    return Response(content='Data recieved', status_code=CREATED)


@app.post("/register")
async def register(user: User) -> Response:
    """Register user.

    Args:
        user (User): dict with user data.

    Returns:
        Response: request response.
    """
    data_from_db = register_in_db(user.to_dict())
    return Response(content=data_from_db[0], status_code=data_from_db[1])


@app.post("/auth")
async def auth(user: User) -> Response:
    """Authentificate user.

    Args:
        user (User): dict with user data.

    Returns:
        Response: request response.
    """
    data_from_db = check_auth(user.to_dict())
    return Response(content=data_from_db[0], status_code=data_from_db[1])


@app.put("/update")
async def update(user: UserInGame) -> Response:
    """Update user.

    Args:
        user (UserInGame): dict with user data.

    Returns:
        Response: request response.
    """
    data_from_db = update_db(user.to_dict())
    return Response(content=data_from_db[0], status_code=data_from_db[1])


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1')
