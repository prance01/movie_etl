import os
import csv
import time 
import codecs 
import xml.etree.ElementTree as etree
import pandas as pd 
import logging 
from settings import DATA_FOLDER
from pandas.io.json import json_normalize 
 
#create a logger 
logger= logging.getLogger()
logger.setLevel(logging.INFO) 

#%%
class Extraction:
   def __init__(self):
      # define file paths 
      self.data_folder = DATA_FOLDER
      self.wiki_xml_file = "enwiki-latest-abstract.xml"
      self.wiki_output_file = os.path.join(self.data_folder,"wiki_data.csv")
      self.top1000_movies_path = os.path.join(self.data_folder, "top1000_movies.csv")
      self.top1000_wiki_path = os.path.join(self.data_folder, "top1000_wiki.csv") 

   # extract the wiki data from XML to CSV
   def get_wiki_data(self):
      logging.info('Extract the wiki data from XML to CSV.')
      vaildCount = 0
      invaildCount = 0 
   
      # get the xml file path 
      wiki_xml_path = os.path.join(self.data_folder, self.wiki_xml_file)
      
      # write the XML data into CSV file 
      with codecs.open(self.wiki_output_file, "w") as wikiLinks:
         wikiLinksWriter = csv.writer(wikiLinks, quoting=csv.QUOTE_MINIMAL)
         wikiLinksWriter.writerow(['title','wiki_link','wiki_abstract']) 

         for event, element in etree.iterparse(wiki_xml_path, events=('start', 'end')):
            if event == 'start':
               if element.tag == 'title' and element.text != None:
                  title = element.text.split(": ")[-1]
               elif element.tag == 'url' and element.text != None:
                  wiki_link = element.text
               elif element.tag == 'abstract' and element.text != None:
                  wiki_abstract = element.text
                  wikiLinksWriter.writerow([title,wiki_link,wiki_abstract]) 
                  vaildCount += 1 
               else:
                  invaildCount += 1
            element.clear()

         # show numbers of vaildCount and invaildCount
         logging.info(f"vaildCount: {vaildCount}")
         logging.info(f"invaildCount: {invaildCount}")
         
      wiki_output = pd.read_csv(self.wiki_output_file)

      # remove duplicated title and url   
      wiki_output = wiki_output.drop_duplicates(subset=['title'])
   
      return wiki_output


   def get_movie_data(self):
      logging.info('Select the top 1000 movies by the ratio of revenue to budget.')
      
      df_movies_metadata = pd.read_csv(os.path.join(self.data_folder,"movies_metadata.csv"))
      df_movies_ratings = pd.read_csv(os.path.join(self.data_folder,"ratings.csv"))
 
      """Data Cleaning"""
      # change columns from "object" to "numeric"  for calculating the ratio 
      cols = ['budget', 'revenue']
      df_movies_metadata[cols] = df_movies_metadata[cols].apply(pd.to_numeric, errors='coerce', axis=1)
      
      # filter poor quality data with conditions 
      df_movies_metadata = df_movies_metadata.loc[(df_movies_metadata['original_language'] == 'en')& (df_movies_metadata['status'] == 'Released') & (df_movies_metadata['revenue'] > 0) & df_movies_metadata['budget'] > 0 ]

      # select relevant columns 
      movies_metadata = df_movies_metadata.loc[:,['id','original_title','budget','revenue','release_date','production_companies']]

      # extract movie releasing year from release_date column 
      movies_metadata['year'] = pd.DatetimeIndex(movies_metadata['release_date']).year 
      
      # convert budget and revenue in millions 
      movies_metadata['revenue_mil'] = movies_metadata['revenue']/100000
      movies_metadata['budget_mil'] = movies_metadata['budget']/100000

      # filter poor quality data with conditions 
      movies_metadata = movies_metadata.loc[movies_metadata['budget_mil'] > 1.0]

      # calculate the ratio of revenue to budget 
      movies_metadata['ratio'] = movies_metadata['revenue_mil']/movies_metadata['budget_mil']
      # sorting the ratio from largest (descending)
      movies_metadata = movies_metadata.sort_values(by=['ratio'],ascending=False)

      # extract companies data
      companies = []
      for i in movies_metadata["production_companies"].tolist():
         if(len(i) > 2):
            companies.append(eval(i)[0]['name'])
         else:
            companies.append("Null")
      movies_metadata["companies"] = companies

      # select top 1000 by ratio 
      top1000_movies = movies_metadata.head(1000)

      # get top 1000 movies' rating by joining "df_movies_ratings"
      top1000_movies['id'] = top1000_movies['id'].apply(int)

      # calculate the average rating of each movie 
      movies_avg_rating = df_movies_ratings.groupby(['movieId'])['rating'].mean().round(2)       
      top1000_movies_ratings = top1000_movies.merge(movies_avg_rating,how='left', left_on = 'id', right_on='movieId')
      
      # rename columns 
      top1000_movies_ratings.columns = ['production_company' if x=='companies' else x for x in top1000_movies_ratings.columns]
    
      # get relevant columns 
      columns = ['original_title','year','budget','revenue', 'ratio','rating','production_company']
      top1000_movies_output = pd.DataFrame(top1000_movies_ratings, columns=columns)
      
      # round values to decimal 2 places
      top1000_movies_output = top1000_movies_output.round(2)
      
      # export top1000_movies as a csv file 
      top1000_movies_output.to_csv(self.top1000_movies_path, encoding='utf-8', index=False)
      
      return top1000_movies_output
 