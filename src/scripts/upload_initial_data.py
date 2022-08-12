from ..utils.takichai_api import TakichaiAPI
from ..utils.meta_parser import MetadataParser
from ..utils.song import Song

def get_songs(folder):
  p = MetadataParser(folder_path=folder)
  songs = []
  for meta in p.getItemsMetadata():
    songs.append(Song(meta))
  return songs

def main():
  FOLDER = r'C:\Personal\dev\taller-mobile\takichai-recomendations\data\songs'

  songs = get_songs(FOLDER)
  
  api = TakichaiAPI(email="sasukenny@gmail.com", password="Hola12345")
  
  for song in songs:
    api.upload_song(song)


if __name__ == '__main__':
  pass
