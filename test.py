import pandas as pd
import json

df1=pd.read_json("output_1.json")

df2=pd.read_json("output_2.json")

df=df1.append(df2,ignore_index=True)

#print(df.head())
author_name = "Martin Luther King, Jr."
print(df.loc[df['author'] == author_name])

for index, row in df.iterrows():
    if row['author'] == str(author_name):
        print("\n"+ row['text'] +"\n"+ row['author'])
