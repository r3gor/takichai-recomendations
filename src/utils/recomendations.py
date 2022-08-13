from .ml_algorithm import ML
from src.utils.takichai_api import TakichaiAPI

class Recomendations:

  def __init__(self):
    self._api = TakichaiAPI(email="sasukenny@gmail.com", password="Hola12345")
    self._songs = self._api.get_songs()
    self._ml = ML(self._songs)

  def get_recomendations(self, items=10):
    return sorted(self._songs, key=lambda s: int(s['popularity']), reverse=True)[:items]

  def get_recomendations_by_songId(self, song_id: str, items=10):
    ids = self._ml.generate_recommendation(items, 'cos', by_songId=song_id)
    songs = list(map(lambda song_id: [s for s in self._songs if s['songId']==song_id][0], ids))
    return songs

  def get_recomendations_by_name(self, song_name: str, items=10):
    return self._ml.generate_recommendation(items, 'cos', by_name=song_name)

  
