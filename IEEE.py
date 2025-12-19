import pandas as pd
import requests

df = pd.read_excel("Boolean_keywords.xlsx", sheet_name="IEEE")
# print(df)
API = "ue98tmgmz8htdtk83693sw"
URL = r"https://ieeexploreapi.ieee.org/api/v1/search/articles"
ndf = pd.DataFrame(columns=df.columns)
ndf['Concept Group'] = df['Concept Group']

for c, d in df.items():
    if ((c != "Core Terms (used in all domains)") and (c != "Concept Group")):
        for r in range(len(d)):
            print(r)
            params = {
                "apikey": API,
                'querytext': d[r]
            }
            response = requests.get(URL,params=params)
            print(response.status_code)
          # data = response.json()
            # ndf.loc[r,c] = data.get('total_records',0)
# print(ndf)