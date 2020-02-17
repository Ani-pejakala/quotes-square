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
import random

st.title('Scrapping quotes from BrainyQuotes and GoodReads!')
t = st.text_input("Enter a topic to scrap quotes")
start = st.button("Get Quotes")
showdf = st.sidebar.checkbox('Show raw dataframe')
showqo = st.checkbox('Show quotes and authors')
seed = st.text_input("Enter length of quote to be generated")
genqo = st.button("Generate Quote")
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

def makestring(df, length):
    contents = ""
    
    for index, row in df.iterrows():
        contents = contents+"".join(row['text']).lstrip().replace("\"",' ')
    
    translator=str.maketrans('','',punctuation)
    data=contents.translate(translator)
   
    #'''Make a rule dict for given data.'''
    rule = {}
    words = data.split(' ')
    context = 2
    index = context
 
    for word in words[index:]:
        key = ' '.join(words[index-context:index])
        if key in rule:
            rule[key].append(word)
        else:
            rule[key] = [word]
        index += 1   
    #'''Use a given rule to make a string.'''
    oldwords = random.choice(list(rule.keys())).split(' ') #random starting words
    string = ' '.join(oldwords) + ' '
 
    for i in range(length):
        try:
            key = ' '.join(oldwords)
            newword = random.choice(rule[key])
            string += newword + ' '
 
            for word in range(len(oldwords)):
                oldwords[word] = oldwords[(word + 1) % len(oldwords)]
            oldwords[-1] = newword
 
        except KeyError:
            return string
    return string


if start and str(t)=="":
    st.error("Please enter a topic... and try again")

if str(t) and not str(t).isspace():
    df = scrap_quotes(str(t))

    if showdf:
        st.dataframe(df)

    if genqo:
        st.write(makestring(df, int(seed)))

    if showqo:
        for index, row in df.iterrows():
            st.write("\n"+ row['text'] +"\n"+ row['author'])
    
    if searchba:
        st.header("Showing all quotes by %s"%str(author_name))
        df1 = df[df['author'].str.contains(author_name)]
        for index, row in df1.iterrows():
            st.write("\n"+ row['text'] +"\n"+ row['author'])
        if len(df1.index)==0:
            st.error("No quotes found for %s"%author_name)
 

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
