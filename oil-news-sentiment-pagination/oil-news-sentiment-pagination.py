import time
import pandas as pd
import lseg.data as ld
import warnings
from datetime import datetime
warnings.filterwarnings("ignore", category=FutureWarning)

chunks = [] # lists are computationally faster than dataframes
END = pd.to_datetime('2026-03-08') # turns readable str to datetime datatype
STOP_DATE = pd.to_datetime('2022-03-08') 

ld.get_config()["http.request-timeout"] = 120 # protect from timeout error
start_time = time.time() # start the clock
while True:    
    chunk = ld.news.get_headlines(
        query = 'Topic:CRU AND Language:LEN',
        end = END,
        count = 500
    ) 

    chunks.append(chunk.headline)  
    END = chunk.index.min()
    print(datetime.now().strftime("%H:%M:%S.%f")) # the stopwatch
    
    
    if chunk.empty or END <= STOP_DATE: 
        break

end_time = time.time() # stop the clock
duration = end_time - start_time 

# clean way to turn list to df
chunks_df = pd.concat(chunks).drop_duplicates() 
print(f"\n{duration} seconds")
print(f"{len(chunks_df)} obs.\n")
print(chunks_df.tail())

chunks_df.to_csv("crude_oil_headlines_raw.csv")
