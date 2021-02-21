import os
import time
import psycopg2
import pandas as pd 
import sqlalchemy
import logging 
from transform import Transformation
from settings import DB_URI,DB_TABLE
from model import Session, MovieModel

#create a logger 
logger= logging.getLogger()
logger.setLevel(logging.INFO) 

class Load:  
   def __init__(self):
      self.db_url = DB_URI
      self.db_table = DB_TABLE

   def export_pg_table(self):
      logging.info('Loading data from Transformation module.')
      # get the top 1000 movie data  
      movie_data = Transformation().data_merging()

      # convert dataframe into dict for commiting rows of data
      movie_records = movie_data.to_dict(orient='records')

      # export data to postgres db 
      logging.info('Start to commit top 1000 movie data to PostgresDB.')
      
      # open the session
      session = Session()
      
      # load the dataframe into the table in one bulk
      try:
         count = 0 
         # connection.execute(target_table.insert(),movie_records) 
         for record in movie_records:
            movie_row = MovieModel(title=record['title'],year=record['year'],
                                   budget=record['budget'],revenue=record['revenue'],
                                   ratio= record['ratio'],rating=record['rating'],
                                   production_company= record['production_company'],
                                   wiki_link = record['wiki_link'],
                                   wiki_abstract = record['wiki_abstract']
                                   )
            session.add(movie_row)
            count += 1 
         # merge all the rows as one 
         session.merge(movie_row)
         # try to commit the data 
         session.commit()
         logging.info(f'Commited no. of {count} rows.')
      except Exception as e:
         logging.error(traceback.format_exc())
         raise e
      finally:
         # close the session
         session.close()
         logging.info(f'Close session.')
      return count

if __name__ == '__main__': 
   # log the processing time
   start_time = time.time()
   print("Start time:", start_time)
   Load().export_pg_table()
   time_took = time.time() - start_time 
   print("End time:",time.time())
   print("Processing time:", time_took)