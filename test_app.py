import requests
from dateutil.parser import parser
from app import create_app
import os
import unittest
import json
from models import setup_db, Movie, Actor
from flask_sqlalchemy import SQLAlchemy

ep_token=os.environ["EP_JWT"]

ca_token=os.environ["CA_JWT"]

cd_token=os.environ["CD_JWT"]

tokens={
    "ca":ca_token,
    "cd":cd_token,
    "ep":ep_token,
}



def getAuthHeaders(role):
    return {"Authorization":"bearer {}".format(tokens[role])}



class CinemaTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.app.app_context().push()
        self.client = self.app.test_client
        self.database_path = os.environ.get('DATABASE_URL_TEST')
        setup_db(self.app, self.database_path)

        self.movie = {
            "title": "Interstellar",
            "release_date": "2020-04-30T04:00:00.000Z",
        }
        self.actor = {
            "name": "Abdulaziz",
            "age": 21,
            "gender": "male",
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        pass

    def test_get_movies(self):
        res = self.client().get("/movies",
                                headers=getAuthHeaders("ep"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["movies"])
        self.assertTrue(len(data["movies"]))

    def test_405_get_movies(self):
        res = self.client().get("/movies/513513",
                                headers=getAuthHeaders("ep"))
        data = res.json

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

    def test_get_actors(self):
        res = self.client().get("/actors",
                                headers=getAuthHeaders("ep"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["actors"])
        self.assertTrue(len(data["actors"]))

    def test_405_get_actors(self):
        res = self.client().get("/actors/311",
                                headers=getAuthHeaders("ep"))
        data = res.json
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

    def test_create_movie(self):
        res = self.client().post("/movies", json=self.movie,
                                 headers=getAuthHeaders("ep"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_400_create_movie(self):
        res = self.client().post('/movies',
                                   headers=getAuthHeaders("ep"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')
        
    def test_403_ca_create_movie(self):
        res = self.client().post('/movies',
                                   headers=getAuthHeaders("ca"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'],
                         'Permission not found.')
        self.assertEqual(data['message']['code'], 'unauthorized')
        
    def test_403_cd_create_movie(self):
        res = self.client().post('/movies',
                                   headers=getAuthHeaders("cd"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'], 
                         'Permission not found.')
        self.assertEqual(data['message']['code'], 'unauthorized')

    def test_create_actor(self):
        res = self.client().post("/actors", json=self.actor,
                                 headers=getAuthHeaders("ep"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_400_create_actor(self):
        res = self.client().post('/actors',
                                   headers=getAuthHeaders("ep"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')
        

    def test_delete_movie(self):

        dummyMovie = Movie(
            title=self.movie["title"],
            release_date=self.movie["release_date"],
            )
        dummyMovie.insert()

        dummyMovieId = dummyMovie.id

        res = self.client().delete("/movies/{}"
                                   .format(dummyMovieId),
                                   headers=getAuthHeaders("ep"))
        
        data = json.loads(res.data)
        deletedMovie = Movie.query.filter(
            Movie.id == dummyMovieId).one_or_none()

        self.assertEqual(deletedMovie, None)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], dummyMovieId)

    def test_404_delete_movie(self):
        res = self.client().delete('/movies/98131389',
                                   headers=getAuthHeaders("ep"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')
        
    def test_403_ca_delete_movie(self):
        res = self.client().delete('/movies/98131389',
                                   headers=getAuthHeaders("ca"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'], 
                         'Permission not found.')
        self.assertEqual(data['message']['code'], 'unauthorized')
        
    def test_403_cd_delete_movie(self):
        res = self.client().delete('/movies/98131389',
                                   headers=getAuthHeaders("cd"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'], 
                         'Permission not found.')
        self.assertEqual(data['message']['code'], 'unauthorized')

    def test_delete_actor(self):

        dummyActor = Actor(name=self.actor["name"], age=self.actor["age"],
                           gender=self.actor["gender"])
        dummyActor.insert()

        dummyActorId = dummyActor.id

        res = self.client().delete("/actors/{}".format(dummyActorId),
                                   headers=getAuthHeaders("ep"))
        data = json.loads(res.data)
        deletedActor = Actor.query.filter(
            Actor.id == dummyActorId).one_or_none()

        self.assertEqual(deletedActor, None)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], dummyActorId)
        

    def test_404_delete_actor(self):
        res = self.client().delete('/actors/98131389',
                                   headers=getAuthHeaders("ep"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')
        
    def test_403_cd_delete_movie(self):
        res = self.client().delete('/movies/98131389',
                                   headers=getAuthHeaders("cd"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'],
                         'Permission not found.')
        self.assertEqual(data['message']['code'], 'unauthorized')

    def test_update_movie(self):
        dummyMovie = Movie(
            title=self.movie["title"],
            release_date=self.movie["release_date"])
        dummyMovie.insert()

        updated_data = {
            "title": "Sound of Matel"
        }
        headers={'Content-Type': 'application/json'}
        headers.update(getAuthHeaders("ep"))
        res = self.client().patch("/movies/{}".format(dummyMovie.id),
                                  data=json.dumps(updated_data), 
                                  headers=headers)
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']["title"], updated_data["title"])

    def test_404_update_movie(self):
        res = self.client().patch("/movies/124251",
                                  headers=getAuthHeaders("ep"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_update_actor(self):
        dummyActor = Actor(name=self.actor["name"], age=self.actor["age"],
                           gender=self.actor["gender"])
        dummyActor.insert()

        updated_data = {
            "name": "Saud"
        }
        headers={'Content-Type': 'application/json'}
        headers.update(getAuthHeaders("ep"))
        res = self.client().patch("/actors/{}".format(dummyActor.id),
                                  data=json.dumps(updated_data),
                                  headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']["name"], updated_data["name"])
        self.assertEqual(data['actor']["age"],
                         dummyActor.age)
        self.assertEqual(data['actor']["gender"],
                         dummyActor.gender)

    def test_404_update_actor(self):
        res = self.client().patch("/actors/124251",
                                  headers=getAuthHeaders("ep"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

        # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
