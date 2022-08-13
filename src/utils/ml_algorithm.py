from pandas import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import sigmoid_kernel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing

from .utils import stime_to_seconds
from .utils import normalize_str

class ML:

  def __init__(self, songs):
    self._songs = songs
    self._preprocesing()
    self._proccess()

  def _preprocesing(self):
    data = pd.DataFrame.from_records(self._songs)

    feature_cols = [
      "name", "songId", "genre", "year",
      "popularity", "duration", "instrumental", "mood"
    ]

    self._df = data[feature_cols]

    self._df['genre'] = self._df['genre'].apply(normalize_str)
    self._df['mood'] = self._df['mood'].apply(normalize_str)
  
    df_numeric = pd.DataFrame()
    df_numeric['popularity']      = self._df['popularity']
    df_numeric['duration']        = self._df['duration'].apply(stime_to_seconds)
    df_numeric["instrumental"]    = self._df["instrumental"].astype(int)
    df_numeric["year"]            = self._df["year"]

    dummies_genre = pd.get_dummies(self._df['genre'], prefix='genre')
    dummies_mood = pd.get_dummies(self._df['mood'], prefix='mood')

    dummies_genre = ML._compound_cols(dummies_genre)
    dummies_mood = ML._compound_cols(dummies_mood)

    self._df_clean = pd.concat([df_numeric, dummies_genre, dummies_mood], axis=1)
    self._df_clean['name'] = self._df['name']
    self._df_clean['songId'] = self._df['songId']

  def _proccess(self):
    feature_cols = list(self._df_clean.columns)
    feature_cols.remove('name')
    feature_cols.remove('songId')

    scaler = MinMaxScaler()
    self.normalized_df = scaler.fit_transform(self._df_clean[feature_cols])

    # Create a pandas series with song titles as indices and indices as series values 
    self._indices_name = pd.Series(self._df_clean.index, index=self._df_clean['name']).drop_duplicates()
    self._indices_songId = pd.Series(self._df_clean.index, index=self._df_clean['songId']).drop_duplicates()

    # Create cosine similarity matrix based on given matrix
    self._cosine_kernel = cosine_similarity(self.normalized_df)
    self._sig_kernel = sigmoid_kernel(self.normalized_df)

  def generate_recommendation(self, items=10, model_type='cos', by_songId=None, by_name=None ):
    """
    Purpose: Function for song recommendations 
    Inputs: song title and type of similarity model
    Output: Pandas series of recommended songs
    """
    if not by_songId and not by_name: return
    model_type = self._cosine_kernel if model_type=='cos' else self._sig_kernel

    # Get song indices
    index = self._indices_name[by_name] if by_name else self._indices_songId[by_songId]

    # Get list of songs for given songs
    score=list(enumerate(model_type[index]))

    # Sort the most similar songs
    similarity_score = sorted(score,key = lambda x:x[1],reverse = True)

    # Select the top-N recommend songs
    similarity_score = similarity_score[1:items+1]
    top_songs_index = [i[0] for i in similarity_score]

    # Top N recommended songs
    key = 'name' if by_name else 'songId'
    top_songs=self._df[key].iloc[top_songs_index]
    
    return list(top_songs.values)

  def _compound_cols(df, sep=';', true_val=1, prefix='genre_'):
    comp_cols = list(filter(
        lambda col: sep in col, 
        df.columns
    ))
    
    for col in comp_cols:
      rows = df[col] == true_val
      subs = col[len(prefix):].split(sep)
      subs_cols = map(lambda s: prefix + s, subs)

      for sub_c in subs_cols:
        df.loc[rows, sub_c] = true_val
    
    return df.drop(comp_cols, axis=1).fillna(0)