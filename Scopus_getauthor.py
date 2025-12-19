from sqlalchemy import create_engine, Column, Integer, String, MetaData, select, update
from sqlalchemy.orm import declarative_base, sessionmaker
import requests
import time
API="565d596b00126cce6cab401be3dc2779"
URL="https://api.elsevier.com/content/abstract/scopus_id/"
### SQL JUNK
Base = declarative_base()
engine = create_engine(
    "postgresql+psycopg2://cgirlamo@localhost:5432/scopus"
)

metadata = MetaData()
metadata.reflect(bind=engine)
params={
    'field':'authors'
}
headers = {
    "X-ELS-APIKey":API,
    "Accept": "application/json"
}
with engine.connect() as conn:
    for table_name, table in metadata.tables.items():
        print(f"\n Table: {table_name}")
        stmt = select(table)
        result = conn.execute(stmt)
        
        for row in result:
            auth_list = ''
            r = row._mapping
            scopus_id = r['SCOPUS_ID']
            url=f"{URL}{scopus_id}"
            response = requests.get(url, headers=headers)
            data = response.json()
            print(response.headers.get("X-RateLimit-Reset", 0))
            # try:
                
            #     authors = data['abstracts-retrieval-response']['coredata']['dc:creator']['author']
            
            #     for x in authors:
            #         x = x['preferred-name']
            #         auth_list = auth_list + f";{x['ce:given-name']},{x['ce:surname']}"
            #     upd = (
            #         update(table)
            #         .where(table.c.id == r['id'])
            #         .values(Author=auth_list)
            #     )
            #     conn.execute(upd)
            #     time.sleep(30)
            # except:
            #     print(response.status_code)