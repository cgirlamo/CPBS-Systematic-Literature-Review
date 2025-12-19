import pandas as pd # import packages
import requests
import json
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
API="565d596b00126cce6cab401be3dc2779" # Scopus API key
URL="https://api.elsevier.com/content/search/scopus" # scopus general search

def get_field(x,key): # this function allows us to get value's from the API JSON, or return None if they don't exist
    return x.get(key,None)

def create_table_class(tablename): # this is a function to create SQL table to hold results 
    return type(
        tablename,
        (Base,),
        {
            "__tablename__": tablename,
            "id": Column(Integer, primary_key=True, autoincrement=True),
            "Title": Column(String),
            "Author": Column(String),
            "Date": Column(String),
            "Volume": Column(String),
            "Pages": Column(String),
            "DOI": Column(String),
            "SCOPUS_ID": Column(String)}
    )

df = pd.read_excel('Boolean_keywords.xlsx',sheet_name="Scopus") # Excel file with keywords
code = pd.read_excel("Boolean_keywords.xlsx",sheet_name="coding") # coding names for out - csv files at Scopus/*.csv
ndf = pd.DataFrame(columns=df.columns) # empty df - not sure if needed
ndf['Concept Group'] = df['Concept Group'] # empty df Concept groups
entries = {} # entries dictionary 
count = 25 # count of entries per page - api only returns a certain amount of results 
### SQL JUNK
Base = declarative_base() # make sql base
engine = create_engine( # create engine to existing sql database
    "postgresql+psycopg2://cgirlamo@localhost:5432/scopus"
)
metadata = MetaData() # create function to get metadata
metadata.reflect(bind=engine) # get metadata on sql
metadata.drop_all(bind=engine) # drop all tables
Session = sessionmaker(bind=engine) # make session 
session = Session()

for c, d in df.items(): # cycle through the Boolean Strings 
    if (c != "Concept Group"): # don't use the concept group column
        for r in range(len(d)): # cycle through the index
            tablename = code.loc[r,c] # get the table name from the code df
            
            User = create_table_class(tablename) # create the table 
            try: # try statement 
                print(c,r) # print column and row numner 
                if pd.isna(d[r]): # if it's NA
                    ndf.loc[r,c] = "NA" # return NA
                else: 
                    Base.metadata.create_all(engine) # commit the table creation
                    params = { # set parameters for API call 
                        "apiKey": API, # apiKey
                        'query': d[r] # query
                    }
                    response=requests.get(URL,params=params) # raw response
                    data = response.json() # convert the response to Json
                    results = data['search-results']['opensearch:totalResults'] # filter through json results
                    start=0 # the number that the json will start at, i.e. if it's 0 it will start at the first record, if 
                    # it's 25 it will start at the 26th record
                    for x in range(int(int(results)/count) + 1): # cycle through each of the pages in the json
                        params = { # updated params
                        "apiKey": API,
                        'query': d[r],
                        'count': str(count), # count, will always be the max of 25
                        'start':str(start) # start, will be the same as the previous start + 25
                        }
                        response2 = requests.get(URL,params=params) # get the raw response again
                        data2 = response2.json() # get the json
                        entries = data2['search-results']['entry'] # get the entry
                        start +=count # update the start counter 
                    
                        for x in entries:
                        
                            print(get_field(x,'dc:title'))
                            new_entry=User(Title=get_field(x,"dc:title"),
                                           Author=get_field(x,"dc:creator"),
                                           Date=get_field(x,"prism:coverDate"),
                                           Volume=get_field(x,"prism:volume"),
                                           Pages=get_field(x,"prism:pageRange"),
                                        DOI=get_field(x,"prism:doi"),
                                        SCOPUS_ID=get_field(x,"dc:identifier"))
                            session.add(new_entry)
                        session.commit()
                        
                    
                    
            except KeyError:
                print("Something is wrong")
                

# with open('test.json','w',encoding='utf-8') as f:
#     json.dump(data,f,indent=2)
# ndf.to_csv('Scopus_results.csv')

# with open('entries.json','w') as f:
#     json.dump(entries, f,indent=4)