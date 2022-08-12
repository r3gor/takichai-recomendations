from .song import Song
import requests

DEFAULT_IMG = "data/img/default.jpg"

class TakichaiHttp:
  URL = 'https://takichai-backend.herokuapp.com'
  HEADERS = {}

  def login(email, password):
    res =  requests.post(f"{TakichaiHttp.URL}/api/users/login", 
      headers = TakichaiHttp.HEADERS,
      json = { "email": email, "password": password },
    ).json()

    if res.get('ok'):
      TakichaiHttp.HEADERS['Authorization'] = 'Bearer ' + res.get('token')

    print("[login]\t ok:", res.get('ok'), " \t|", email)
    
    return res

  def post_song(payload, files):

    res = requests.post(f"{TakichaiHttp.URL}/api/songs",
      headers = TakichaiHttp.HEADERS,
      data = payload,
      files = files,
    ).json()

    print("[post_song]\t ok:", res.get('ok'), " |\t", payload.get('name'))

    if res.get('ok') == False:
      print(res)

    return res


class TakichaiAPI:
  
  def __init__(self, email, password):
    TakichaiHttp.login(email, password)
  
  def upload_song(self, song: Song):
    file_from_path = lambda path: path.split('/')[-1] or path.split('\\')[-1] 
    files = [
      ('img',  (file_from_path(song.song)  , open(DEFAULT_IMG,'rb'), 'image/jpeg')),
      ('song', (file_from_path(DEFAULT_IMG), open(song.song, 'rb') , 'audio/mpeg'))
    ]
    TakichaiHttp.post_song(payload=song.serialize(), files=files)
