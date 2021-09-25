# Casting Agency 


## Motivation

This project aims to consolidate the knowledge gained from the fullstack nanodegree.

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Testing the API locally

in order to run the test locally run the following commands:

    source setup.sh
    python test_app.py

### Installing Python Dependencies

Navigate to the fullstack_capstone folder and install python package dependencies by running:

    pip3 install -r requirements.txt

## Testing the API on Heroku

The host address of the Heroku deployment is `https://capstone445.herokuapp.com/`.

## Endpoints

### GET /movies

Fetch list of movies

#### Required permission

`get:movies`

### Response

A list of movie objects

    {
    "movies": [
        {
            "actors": [],
            "id": 1,
            "release_date": "Thu, 30 Apr 2020 04:00:00 GMT",
            "title": "Interstaler"
        }
    ],
    "success": true
    }

### GET /actors

`Fetch list of actors`

#### Require permission

`get:actors`

#### Response

A list of actor objects.

    {
    "actors": [
        {
            "age": 21,
            "gender": "male",
            "id": 2,
            "movie_id": 1,
            "name": "Abdulaziz"
        }
    ],
    "success": true
    }

### POST /movies

Creates a new movie in the database.

#### Required permission

`post:movie`

#### Request payload

| key          | Description                                 |
| ------------ | ------------------------------------------- |
| title        | The title of the movie                      |
| release_date | The release date of the movie in ISO format |

Example:

    {
    "title": "Interstaler",
    "release_date": "2020-04-30T04:00:00.000Z"
    }

All of the keys and their corresponding data must be included in the request.

#### Response payload of submitting new questions

Success message and the newly created movie

    {
    "movie": {
        "actors": [],
        "id": 2,
        "release_date": "Thu, 30 Apr 2020 04:00:00 GMT",
        "title": "Interstaler"
    },
    "success": true
    }

### POST /actors

Creates a new actor in the database.

#### Required permission

`post:actor`

#### Request payload

| key      | Description                     |
| -------- | ------------------------------- |
| name     | The name of the actor           |
| age      | The age of the actor            |
| gender   | The actor's gender              |
| movie_id | The movie must exist in advance |

All of the keys and their corresponding data must be included in the request.
Example:

    {
    "name":"Abdulaziz",
    "age":21,
    "gender":"male",
    "movie_id":1
    }

#### Response payload of submitting new questions

Success message and the newly created actor

    {
    "actor": {
        "age": 21,
        "gender": "male",
        "id": 2,
        "movie_id": 1,
        "name": "Abdulaziz"
    },
    "success": true
    }

### PATCH /movies

Update a movie in the database.

#### Required permission

`update:movie`

#### Request payload

| key          | Description                                 |
| ------------ | ------------------------------------------- |
| title        | The title of the movie                      |
| release_date | The release date of the movie in ISO format |

Example:

    {
    "title":"Sound of Matel"
    }

#### Response payload of submitting new questions

Success message and the updated movie object

    {
    "movie": {
        "actors": [],
        "id": 1,
        "release_date": "Thu, 30 Apr 2020 04:00:00 GMT",
        "title": "Sound of Matel"
    },
    "success": true
    }

### PATCH /actors

Update an actor in the database.

#### Required permission

`update:actor`

#### Request payload

| key      | Description                     |
| -------- | ------------------------------- |
| name     | The name of the actor           |
| age      | The age of the actor            |
| gender   | The actor's gender              |
| movie_id | The movie must exist in advance |

Example:

    {
    "name":"Ali"
    }

#### Response payload of submitting new questions

Success message and the newly updated actor

    {
    "actor": {
        "age": 21,
        "gender": "male",
        "id": 2,
        "movie_id": 1,
        "name": "Ali"
    },
    "success": true
    }

### DELETE /movies/<movie_id>

Deletes the specified movie.

#### Required permission

`delete:movie`

#### Response payload

Success message and the deleted movie id.

### DELETE /actors/<actor_id>

Deletes the specified actor.

#### Required permission

`delete:actors`

#### Response payload

Success message and the id of the deleted actor.

## RBAC

The API uses [Auth0](https://auth0.com/) to authenticate users with Javascript Web Tokens.

Three roles are defined with the following permissions:
| Role | Permissions |
|--|--|
| Casting Assistant | `get:actors` `get:movies` |
| Casting Director | `get:actors` `get:movies` `delete:actor` `post:actor` `update:actor` `update:movie`|
| Executive Producer | `get:actors` `get:movies` `delete:actor` `post:actor` `update:actor` `update:movie` `delete:movie` `post:movie`
|

Tokens can be requested by sending a POST message to `https://dev-btox-ysw.us.auth0.com/oauth/token` with the following JSON payload:

    {
        "client_id": "JGsmO5DcCOdlDFEcv3cQolLTrHU3xuq0",
        "client_secret": "WVmK6DxYn8CO5Jw6wWEKeEKV46uGsL-kVytNbV4RnScv1JPHGqIL4K5Dwwyfxh_F",
        "audience": "https://agency-api",
        "grant_type": "password",
        "username": <username>,
        "password": <password>
    }

The following username and password pairs can be used for the roles defined above:

| Role                | Username                     | Password            |
| ------------------- | ---------------------------- | ------------------- |
| Casting assistant   | executive-assiss@gmail.com   | casting-assistant1  |
| Casting director    | executive-direct@gmail.com   | casting-director1   |
| .Executive producer | executive-producer@gmail.com | executive-producer1 |

The tokens recieved this way must be included in the `Authorization` header of a request sent towards the API endpoints.

A jwt token can be obtained by login using the above credentials into the following [link](https://dev-btox-ysw.us.auth0.com/authorize?response_type=token&client_id=JGsmO5DcCOdlDFEcv3cQolLTrHU3xuq0&redirect_uri=https://127.0.0.1:8080/login-result&state=STATE&audience=https://agency-api)

## Setup Heroku

1.  Install Heroku CLI: `brew install heroku/brew/heroku`
2.  Login to Heroku: `heroku login`
3.  Create app at Heroku: `heroku create my-app-name`
4.  Set Procfile: `echo "web: gunicorn app:APP" > Procfile`
5.  Commit changes and push to origin
6.  Push to Heroku: `git push heroku master`
7.  Add Postgres DB: `heroku addons:create heroku-postgresql:hobby-dev`
8.  At Heroku, DB connection url is taken from env var `DATABASE_URL`
9.  Upgrade DB: `heroku run flask db upgrade`
