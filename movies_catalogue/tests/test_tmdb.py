import tmdb_client, pytest
from unittest.mock import Mock
from main import app

requests_mock = Mock()
response = requests_mock.return_value


def test_get_movies_list(monkeypatch):
   mock_movies_list = ['Movie 1', 'Movie 2']

   response.json.return_value = mock_movies_list
   monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

   movies_list = tmdb_client.get_movies_list(list_type="popular")
   assert movies_list == mock_movies_list


def test_get_single_movie(monkeypatch):
   mock_movie = 'Movie1'

   response.json.return_value = mock_movie
   monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

   movie = tmdb_client.get_single_movie(movie_id=1)
   assert movie == mock_movie


def test_get_single_movie_cast(monkeypatch):
   mock_cast = ["Cast"]

   response.json.return_value = mock_cast
   monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

   cast = tmdb_client.get_single_movie(movie_id=1)
   assert cast == mock_cast



def test_call_tmdb_api(monkeypatch):
   mock_endpoint = "/movie"

   response.json.return_value = mock_endpoint
   monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

   endpoint = tmdb_client.call_tmdb_api(endpoint='/')
   assert endpoint == mock_endpoint


@pytest.mark.parametrize('list_type', (
   ("popular"),
   ("top_rated"),
   ("upcoming"),
   ("now_playing"),
))
def test_homepage(monkeypatch, list_type):
   api_mock = Mock(return_value={'results': []})
   monkeypatch.setattr("tmdb_client.call_tmdb_api", api_mock)

   with app.test_client() as client:
       response = client.get('/')
       assert response.status_code == 200

