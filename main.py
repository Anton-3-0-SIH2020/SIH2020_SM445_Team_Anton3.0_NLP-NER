from NewsScraper import Money_Control_Scraper
import sqlite3
import csv
import spacy
import pickle
import en_core_web_sm
import pandas as pd
import nltk
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

#Pre-processing the text
def text_process(text):
    #Remove the punctuation
    #Remove the stopwords
    #Return list of clean text
    text=''.join([char for char in text if char not in string.punctuation])
    return [word for word in text.split() if word.lower() not in stopwords.words('english')]

# Initializing the database
def initializeDb():
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    create_table = 'CREATE TABLE IF NOT EXISTS news (headline text,content text,link text,category text)'
    c.execute(create_table)
    conn.commit()
    conn.close()

# Creating CSV from the database
def writeDataInCsv():
    with open('news.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Category", "News"])
        conn = sqlite3.connect('news.db')
        c = conn.cursor()
        readData = 'SELECT * FROM news'
        c.execute(readData)
        for row in c:
            writer.writerow([row[3], row[1]])

#Creating DB for new from the news table with only ca related news
def createDbOfCaForNer():
    conn=sqlite3.connect('news.db')
    c=conn.cursor()
    c1=conn.cursor()

    create_table='CREATE TABLE IF NOT EXISTS ca_news (content text,category text,purpose text)'
    c.execute(create_table)

    c.execute('SELECT * FROM news WHERE category="ca"')

    add_item_to_table="INSERT INTO ca_news VALUES(?,?,?)"
    for row in c:
        c1.execute(add_item_to_table,(row[1],'null','null'))

    conn.commit()
    conn.close()

#Getting the type of Ca
def getCaType(news):
    nlp=spacy.load('nlp_model')
    doc = nlp(news)
    for ent in doc.ents:
        print('CA Type: '+ent.text)
    print('----CA----')
    print()

#Getting the general details like the orgainsation and date etc
def getGeneralDetails(news):
    org=''
    ex_date=''
    record_date=''

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(news)
    for ent in doc.ents:
        if(ent.label_=='ORG' and org==''):
            org=ent.text
        elif(ent.label_=='DATE' and record_date==''):
            record_date=ent.text
        elif(ent.label_=='DATE' and ex_date==''):
            ex_date=ent.text
    
    print()
    print('----CA----')
    print('Organisation: '+org)
    print('Ex-Date: '+ex_date)
    print('Record-Date: '+record_date)

#Categorise the news based on
def newsCategoriser(news):
    filename = 'nlp_model_categorizer'
    infile = open(filename,'rb')
    pipeline = pickle.load(infile)
    infile.close()
    predictions = pipeline.predict(pd.Series(news))
    return predictions[0]


if __name__=="__main__":
    # initializeDb()
    # moneyControlScraper=Money_Control_Scraper.MoneyControlScraper()
    # moneyControlScraper.scrapeNews()
    # writeDataInCsv()
    # createDbOfCaForNer()

    news='Shareholders of Torrent Power will consider a proposal for a dividend of Rs 2.20 per share for 2016-17 at its annual general meeting on August 1'
    category=newsCategoriser(news)

    if category=='ca':
        getGeneralDetails(news)
        getCaType(news)

    else:
        print('----NOT CA----')