import os
import json
import time
import pandas as pd 
import logging
from extract import Extraction
from settings import DATA_FOLDER


#create a logger 
logger= logging.getLogger()
logger.setLevel(logging.INFO) 


class Transformation:  
   def __init__(self):
      # define file paths 
      self.data_folder = DATA_FOLDER
      self.output_file = os.path.join(self.data_folder,"top1000_wiki.csv")
      self.extraction = Extraction()

   # merge top 1000 movies data and wiki info
   def data_merging(self):
      logging.info('Start to merge movie data and wiki data.')
      # get top 1000 movies dataframe and wiki dataframe 
      logging.info('Get the top 1000 movies dataframe')
      movie_df = self.extraction.get_movie_data()
      logging.info('Get the wiki info dataframe')
      wiki_df = self.extraction.get_wiki_data()
      
      logging.info('Merge top 1000 movies data and wiki info.')
      # merge top 1000 movies data and wiki info result
      top1000_wiki = movie_df.merge(wiki_df, how='left', left_on='original_title', right_on='title')
      # select relevant columns
      top1000_wiki = top1000_wiki[['original_title','year','budget','revenue','ratio','rating','production_company','wiki_link','wiki_abstract']]
      # rename columns 
      top1000_wiki.columns = ['title' if x=='original_title' else x for x in top1000_wiki.columns]
      
      # export dataframe to csv
      top1000_wiki.to_csv(self.output_file, index=False)

      return top1000_wiki