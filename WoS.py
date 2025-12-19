import pandas as pd
import requests
import json
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker


API = "7959d05fe8d02027abc8629636dafa501cccddd7"
URL = "https://api.clarivate.com/apis/wos-starter/v1/documents"

def get_field(x,key):
    return x.get(key,None)

def create_table_class(tablename):
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
            "DOI": Column(String)
        }
    )
df = pd.read_excel('Boolean_keywords.xlsx', sheet_name="Web Of Science")
code = pd.read_excel('Boolean_keywords.xlsx',sheet_name='coding')
ndf = pd.DataFrame(columns=df.columns)
ndf['Concept Group'] = df['Concept Group']
entries = {}
count = 25
Base = declarative_base()
engine = create_engine(
    "postgresql+psycopg2://cgirlamo@localhost:5432/wos"
)
metadata = MetaData()
metadata.reflect(bind=engine)
metadata.drop_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
headers = {
    "X-ApiKey": API,
    'Accept': "application/json"
}
for c, d in df.items():
    if (c != "Concept Group"):
        for r in range(len(d)):
            tablename = code.loc[r,c]
            
            User = create_table_class(tablename)
            try:
                print(c,r)
                if pd.isna(d[r]):
                    ndf.loc[r,c] = "NA"
                else:
                    Base.metadata.create_all(engine)
                    params = {
                        "db":"WOS",
                        
                        'q': d[r]
                    }
                    response=requests.get(URL,params=params,headers=headers)
                    data = response.json()
                    print(data)
                    # results = data['search-results']['opensearch:totalResults']
                    # for x in range(1,int(int(results)/count) + 1):
                    #     params = {
                    #     "databaseID":"WOS",
                    #     'usrQuery': d[r],
                    #     'count': str(count),
                    #     "page":x
                    #     }
                    #     response2 = requests.get(URL,params=params, headers=headers)
                    #     data2 = response2.json()
                    #     print(data2)
                    #     entries = data2['search-results']['entry']
                    #     start +=count
                    
                        # for x in entries:
                        
                        #     print(get_field(x,'dc:title'))
                        #     new_entry=User(Title=get_field(x,"dc:title"),
                        #                    Author=get_field(x,"dc:creator"),
                        #                    Date=get_field(x,"prism:coverDate"),
                        #                    Volume=get_field(x,"prism:volume"),
                        #                    Pages=get_field(x,"prism:pageRange"),
                        #                 DOI=get_field(x,"prism:doi"))
                        #     session.add(new_entry)
                        # session.commit()
                        
                    
                    
            except KeyError:
                print("Something is wrong")
ndf.to_csv('WOS_results.csv')