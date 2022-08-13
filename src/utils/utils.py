import unidecode
import datetime
import time

normalize_str = lambda s: unidecode.unidecode(s.lower())

def stime_to_seconds(s: str):
  x = time.strptime(s,'%M:%S')
  secs = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
  return int(secs)