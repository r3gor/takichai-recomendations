# name
# year
# description
# genre
# mood
# instrumental
# img
# song

class Song:

  def __init__(self, metadata):
    self.__metadata = metadata

  @property
  def name(self):
    return self.__metadata["T\u00edtulo"]
  
  @property
  def year(self):
    return self.__metadata["A\u00f1o"]

  @property
  def description(self):
    return f'Cover de {self.__metadata["Autores"]} (Album: {self.__metadata["Álbum"]}).'

  @property
  def genre(self):
    return self.__metadata['Género'] or 'Rock'
  
  @property
  def mood(self):
    return 'Melancolía'
  
  @property
  def instrumental(self):
    return False
  
  @property
  def img(self):
    pass
  
  @property
  def song(self):
    return self.__metadata["__path__"]

  def __repr__(self):
    return f"\
      - name:\t {self.name} \n\
      - year:\t {self.year} \n\
      - description:\t {self.description} \n\
      - genre:\t {self.genre} \n\
      - mood:\t {self.mood} \n\
      - instrumental:\t {self.instrumental} \n\
      - img:\t {self.img} \n\
      - song:\t {self.song} \n\
    "

  def serialize(self):
    return {
      "name": self.name,
      "year": self.year,
      "description": self.description,
      "genre": self.genre,
      "mood": self.mood,
      "instrumental": 'true' if self.instrumental else 'false',
      # "img": self.img,
      # "song": self.song,
    }
