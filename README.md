# Project starts up FastAPI server that can recieve data from game.

# About
You can register and authentificate in game, than play in it. In game you contol a small bird(WASD or K_lrud). Telemetry from game is sended on the FastAPI server in real time.

# How install
_$ sudo apt-get update_

_$ git clone https://github.com/Max2288/fly_school_game.git_


# How run
Add .env file with your data

Go to repo and run commands:

_$ docker run -d\
    --name fly_game -p 5333:5432 \
    -v $HOME/postgresql/fly_game:/var/lib/postgresql/fly_game \
    -e POSTGRES_PASSWORD=0000 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_DB=fly_db \
    postgres:15.1_

_$ psql -h 127.0.0.1 -p 5333 -U postgres fly_db -f init_db.ddl (password 0000)_

_$ python3 -m venv ./venv_

_$ . ./venv/bin/activate_

_$ pip install -r requirements.txt_

# After start
Run commands in different terminals

_$ python3 main.py_

_$ python3 game.py_


# .env
## Below should be your data to project
    DB_HOST=database host
    DB_PORT=database port from docker
    DB_USER=database user
    DB_PASSWORD=database password
    DATABASE=database name
Take this data from your docker container

