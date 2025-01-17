import sqlite3
import csv
import spacy
import pickle
import en_core_web_md
import pandas as pd
import nltk
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from Prediction_Pipeline import prediction_pipeline

#Function to clean the text and pre processing it
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
    with open('news_status.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Status", "News"])
        conn = sqlite3.connect('news_status.db')
        c = conn.cursor()
        readData = 'SELECT * FROM ca_news'
        c.execute(readData)
        for row in c:
            if(row[3]!='null' and row[3]!=None):
                writer.writerow([row[3], row[0]])

#Creating DB for new from the news table with only ca related news
def createDbOfCaForNer():
    conn=sqlite3.connect('news.db')
    c=conn.cursor()
    c1=conn.cursor()

    create_table='CREATE TABLE IF NOT EXISTS ca_news (content text,category text,purpose text,announcement_date text,record_date text)'
    c.execute(create_table)

    c.execute('SELECT * FROM news WHERE category="ca"')

    add_item_to_table="INSERT INTO ca_news VALUES(?,?,?,?,?)"
    for row in c:
        c1.execute(add_item_to_table,(row[1],'null','null','null','null'))

    conn.commit()
    conn.close()


#Read all the news from db
def addCaPredictedDataToDb():
    conn=sqlite3.connect('news.db')
    c=conn.cursor()
    read_data='SELECT * FROM news'
    c.execute(read_data)

    conn2=sqlite3.connect('corporate_action.db')
    c1=conn2.cursor()

    add_item_to_table='INSERT INTO predicted_ca VALUES(?,?,?,?,?)'

    for row in c:
        news=row[1]
        print(news)
        pipeline=prediction_pipeline.PredictionPipeline()
        detailList=pipeline.pipeline(news)
        detailList.append(news)
        if(len(detailList)>1):
            if(detailList[0]!=''):
                c1.execute(add_item_to_table,(detailList[0],detailList[1],detailList[2],detailList[3],news))
                conn2.commit()
    conn.close()
    conn2.close()

#Create DB for predicted ca
def createPredictedCaDb():
    conn = sqlite3.connect('corporate_action.db')
    c = conn.cursor()
    create_table = 'CREATE TABLE IF NOT EXISTS predicted_ca (security_name text,category text,purpose text,all_date text,content text)'
    c.execute(create_table)
    conn.commit()
    conn.close()

if __name__=="__main__":

    #Testing a news
    news='BAMPSL Securities is quoting ex-rights today. The company has announced a rights in the ratio of 2:1 at Re 1 per share on March 31, 2011. The record date has been fixed at April 20, 2011.'
    pipeline=prediction_pipeline.PredictionPipeline()
    output=pipeline.pipeline(news)
    output.append(news)
    if(len(output)>1):
        print('----DETAILS----')
        print('NEWS ',news)
        print('ORG: ',output[0])
        print('CA_TYPE: ',output[1])
        print('PURPOSE: ',output[2])
        print('DATE: ',output[3])
        print('----DETAILS----')
        print('----CA----')
    else:
        print('----NO ORG NAME FOUND----')

    # addCaPredictedDataToDb()
        


    # createDbOfCaForNer()

    # writeDataInCsv()