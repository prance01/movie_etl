import os 
import pytest
import pandas as pd
from settings import DATA_FOLDER

# test the final dataframe's shape. It should be 1000 rows and 9 columns.
def test_df_shape():
   df = pd.read_csv(os.path.join(DATA_FOLDER, "top1000_wiki.csv"))
   assert df.shape == (1000,9)

# test if all the columns match the expected result
def test_df_columns():
   df = pd.read_csv(os.path.join(DATA_FOLDER, "top1000_wiki.csv"))
   assert df.columns.tolist() == ['title', 'year', 'budget', 'revenue', 'ratio', 'rating', 'production_company', 'wiki_link', 'wiki_abstract']

# test if all of the movie name and year is unique. The movie name can be same. Eg. Beauty and the Beast 1991 &  Beauty and the Beast 2017 
def test_df_names():
   df = pd.read_csv(os.path.join(DATA_FOLDER, "top1000_wiki.csv"))
   assert df.groupby(['title','year']).size().max() == 1
   
