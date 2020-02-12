import streamlit as st
import json
import pandas as pd
import subprocess
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from wordcloud import WordCloud 
from collections import Counter
from string import punctuation
import re
import string
import nltk
# import spider class
from quotes.spiders import goodreads

st.title('Scrapping quotes from BrainyQuotes and GoodReads!')
t = st.text_input("Enter a topic to scrap quotes")
start = st.button("Get Quotes")
showdf = st.sidebar.checkbox('Show raw dataframe')
showqo = st.checkbox('Show quotes and authors')
showwc = st.sidebar.checkbox('Show word cloud')
showwf = st.sidebar.checkbox("Show tag Frequency")
author_name = st.sidebar.text_input("Search by name of author")
searchba = st.sidebar.button("Search")

@st.cache(suppress_st_warning=True)
def scrap_quotes(t):
    open("output_1.json", 'w').truncate(0)
    open("output_2.json", 'w').truncate(0)
    
    st.text("Scraping quotes based on %s .... Wait a moment"%t)
    topic=t
    spiders = {"goodreads":"output_1.json","brainyquotes":"output_2.json"}
    for spider in spiders:
        subprocess.check_output(['scrapy', 'crawl', "-a","topic=%s"%topic,spider, "-o", spiders[spider]])

    df1=pd.read_json("output_1.json")
    st.success("www.brainyquotes.com\%s crawled successfully"%t)
    df2=pd.read_json("output_2.json")
    st.success("www.goodreads.com\%s crawled successfully"%t)
    df=df1.append(df2,ignore_index=True)
    return df

def text_process(raw_text):
    nopunc = [char for char in list(raw_text) if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    return [word for word in nopunc.lower().split() if word.lower() not in stopwords.words('english')]
    
def makeWordCloud(all_words, color):
    wordfreq = Counter(all_words)
    wordcloud = WordCloud(width=300,
                          height=150,
                          max_words=50,
                          max_font_size=50,
                          relative_scaling=0.5,
                          colormap=color,
                          normalize_plurals=True).generate_from_frequencies(wordfreq)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot()

if str(t) and not str(t).isspace():
    df = scrap_quotes(str(t))

    if showdf:
        st.dataframe(df)

    if showqo:
        for index, row in df.iterrows():
            st.write("\n"+ row['text'] +"\n"+ row['author'])
    
    if searchba:
        st.header("Showing all quotes by %s"%str(author_name))
        #st.write(df.loc[df['author'] == author_name])
        
        for index, row in df.iterrows():
            if row['author'] == author_name:
                st.write("\n"+ row['text'] +"\n"+ row['author'])   

    if showwf:
        freq_words = []
        for ls in df['tags']:
            words = [w for w in ls]
            for word in words:
                freq_words.append(word)
        fd = nltk.FreqDist(freq_words)
        df_fd = pd.DataFrame({'Term': list(fd.keys()),'Frequency': list(fd.values())})
        df_fd = df_fd.nlargest(columns="Frequency", n = 10) 
        df_fd.plot(kind = 'bar', x ='Term', y='Frequency')
        st.write("Showing Top 10 frequently used tags")
        st.pyplot()

    if showwc:
        all_words = []
        df1 = pd.DataFrame()
        df1['tokens'] = df['text'].apply(text_process)
        for line in df1['tokens']:
            all_words.extend(line)
        makeWordCloud(all_words,'Blues')

# scrapy api
#spider_name = "goodreads"
#open("output.json","w").truncate(0)
#subprocess.check_output(['scrapy', 'crawl', spider_name, "-o", "output.json"])
#df = pd.read_csv('quotes.csv')
