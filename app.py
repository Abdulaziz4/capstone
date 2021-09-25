import os
from flask import Flask, json, jsonify, abort, request
from flask_migrate import Migrate
from models import db, setup_db, Movie, Actor
from dateutil import parser
from auth import requires_auth, AuthError

migrate=Migrate()
def create_app():
    app = Flask(__name__)
    db_path_prod =os.environ.get('DATABASE_URL')

    setup_db(app,db_path_prod)

    migrate.init_app(app, db)

    @app.route("/")
    def home():
        
        return jsonify({
        "success": True,
    })

    @app.route("/movies")
    @requires_auth("get:movies")
    def get_movies(payload):
        movies = Movie.query
        return jsonify({
        "success": True,
        "movies": [Movie.format(movie) for movie in movies]
    })


    @app.route("/actors")
    @requires_auth("get:actors")
    def get_actors(payload):
        actors = Actor.query
        return jsonify({
        "success": True,
        "actors": [Actor.format(actor) for actor in actors]
    })


    def noneChecker(value):
        return value is None


    @app.route("/movies", methods=["POST"])
    @requires_auth("post:movie")
    def add_movie(payload):
        body = request.get_json()
        if body is None:
            abort(400)

        title = body.get("title", None)
        plain_date = body.get("release_date", None)
        if title is None or plain_date is None:
            abort(400)

        date = parser.parse(plain_date)
        movie = Movie(title=title, release_date=plain_date)
        movie.insert()
        return jsonify({
            "success": True,
            "movie": movie.format()
         })


    @app.route("/actors", methods=["POST"])
    @requires_auth("post:actor")
    def add_actor(payload):
        body = request.get_json()
        if noneChecker(body):
            abort(400)

        name = body.get("name", None)
        age = body.get("age", None)
        gender = body.get("gender", None)
        movie_id = body.get("movie_id", None)

        if noneChecker(name) or noneChecker(age) or noneChecker(gender):
         abort(400)

        actor = Actor(name=name, age=age, gender=gender,
                      movie_id=movie_id)
        actor.insert()
        return jsonify({
            "success": True,
            "actor": actor.format()
        })


    @app.route("/movies/<id>", methods=["DELETE"])
    @requires_auth("delete:movie")
    def delete_movie(payload, id):
        movie = Movie.query.get_or_404(id)
        try:
            deleted_id = movie.id
            movie.delete()
            return jsonify({
            "success": True,
            "id": deleted_id
        })
        except:
            abort(422)


    @app.route("/actors/<id>", methods=["DELETE"])
    @requires_auth("delete:actor")
    def delete_actor( payload,id):
        actor = Actor.query.get_or_404(id)
        try:
            deleted_id = actor.id
            actor.delete()
            return jsonify({
            "success": True,
            "id": deleted_id
            })
        except:
            abort(422)


    @app.route("/movies/<id>", methods=["PATCH"])
    @requires_auth("update:movie")
    def update_movie(payload,id):
        movie = Movie.query.get_or_404(id)

        body = request.get_json()
        if noneChecker(body):
            abort(400)

        title = body.get("title", None)
        if not noneChecker(title):
            movie.title = title

        plain_date = body.get("release_date", None)
        if not noneChecker(plain_date):
            date = parser.parse(plain_date)
            movie.release_date = date

        movie.update()
        return jsonify({
            "success": True,
            "movie": movie.format()
        })


    @app.route("/actors/<id>", methods=["PATCH"])
    @requires_auth("update:actor")
    def update_actor( payload,id):
        actor = Actor.query.get_or_404(id)

        body = request.get_json()
        if noneChecker(body):
            abort(404)

        name = body.get("name", None)
        if not noneChecker(name):
            actor.name = name

        age = body.get("age", None)
        if not noneChecker(age):
            actor.age = age

        gender = body.get("gender", None)
        if not noneChecker(gender):
            actor.gender = gender

        movie_id     = body.get("movie_id", None)
        if not noneChecker(movie_id):
            actor.movie_id = movie_id

        actor.update()
        return jsonify({
            "success": True,
            "actor": actor.format(),
        })


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unable to process"
        }), 422


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400
        
    @app.errorhandler(405)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405


    @app.errorhandler(AuthError)
    def auth_error_handler(e):
        return jsonify({
            "success": False,
            "error": e.status_code,
            "message": e.error
        }), e.status_code
        
    return app

app=create_app()
