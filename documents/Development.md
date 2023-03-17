# Development

## Contents

- [Introduction](#introduction)
- [DevLogs](#devlogs)
- [Running Locally](#running-locally)
- [Running with Docker](#running-with-docker)

## Introduction

...

## DevLogs

...

## Running Locally

**Note:** For all terminal commands in the following sections, it is assumed that you are starting from the root directory of the project (ie. rpi-controller).

### Frontend

The frontend VueJS app can be run inside a provided development server. One of the benefits of this is that the server hot-reloads everytime the code is changed, so there is no need to restart the server in order to view your changes.

```shell
cd display
npm install    # install all required packages
npm run serve  # start a development server
```

### Backend

First, we need to activate our python virtual environment. Some IDE's will do this for you (like PyCharm); however, some do not (like VSCode), in which case you will need to do it manually.

```shell
venv\Scripts\activate.bat  # Windows
source venv/bin/activate   # Unix or MacOS
```

Once you're python venv has been activated, we can run the backend server by running _main.py_.

```shell
cd server
python main.py
```

Alternatively, you can run uvicorn directly.

```shell
cd server
uvicorn main:app --host 0.0.0.0 --port 8577 --reload
```

Once you're done, you can de-activate your virtual environment.

```shell
deactivate
```

### Redis

...

```shell
docker-compose -f docker-compose-local.yml up --build
```

### Controller

...

## Running with Docker

...
