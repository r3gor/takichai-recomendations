from time import sleep
import win32com.client

class MetadataParser:

  __sh = win32com.client.gencache.EnsureDispatch('Shell.Application',0)

  def __init__(self, folder_path: str):
    self.__ns = self.__sh.NameSpace(folder_path)
    self.features = self.__getFeatures() 

  def __getFeatures(self):
    colnum = 0
    columns = []
    while True:
        colname=self.__ns.GetDetailsOf(None, colnum)
        if not colname:
            break
        columns.append(colname)
        colnum += 1
    return columns

  def getItems(self):
    return self.__ns.Items()

  def getItemMetadata(self, item):
    song = { "__path__": item.Path }
    for i in range(len(self.features)):
      f_name = self.features[i]
      f_value = self.__ns.GetDetailsOf(item, i)
      song[f_name] = f_value
      
    return song

  def getItemsMetadata(self): 
    songs = []
  
    print("[*] reading metadata...")
  
    for item in self.getItems():

      songs.append(self.getItemMetadata(item))
      print('*', end='', flush=True)

    print("\n[*] metadata loaded", "\t items:", len(songs))

    return songs 