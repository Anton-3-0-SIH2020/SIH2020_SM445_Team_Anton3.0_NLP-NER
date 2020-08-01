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

class PredictionPipeline:

    #Function to clean the text and pre processing it
    def text_process(self,text):
        #Remove the punctuation
        #Remove the stopwords
        #Return list of clean text
        text=''.join([char for char in text if char not in string.punctuation])
        return [word for word in text.split() if word.lower() not in stopwords.words('english')]

    #Text cleaning before feeding the data to the model
    def text_cleaning(self,news):
        news=news.replace('Rs','$')
        news=news.replace('Re','$')
        news=news.replace('today','')
        return news

    #Categorise the news based on
    def newsCategoriser(self,news):
        filename = 'nlp_model_categorizer'
        infile = open(filename,'rb')
        pipeline = pickle.load(infile)
        infile.close()
        predictions = pipeline.predict(pd.Series(news))
        return predictions[0]


    def getDetailsFromText(self,news):
        org=''
        date=''
        ca_type=''

        #Getting general information
        nlp = spacy.load('en_core_web_md')
        doc = nlp(news)
        for ent in doc.ents:
            if(ent.label_=='ORG' and org==''):
                org+=ent.text
            elif(ent.label_=='DATE'):
                date+=ent.text+" , "
        
        # print()
        # print('----CA----')
        # print('Organisation: '+org)
        # print('Date: '+date)

        #Getting ca type
        nlp=spacy.load('nlp_model')
        doc = nlp(news)

        for ent in doc.ents:
            ca_type+=ent.text+" , "
        # print('CA Type: '+ca_type)
        # print('----CA----')
        # print()
        return [org,ca_type,date]

    def pipeline(self,news):
        category=self.newsCategoriser(news)
        if category=='ca':
            print('----CA----')
            cleaned_news=self.text_cleaning(news)
            detailList=self.getDetailsFromText(cleaned_news)
            if(detailList[0]!=''):
                return detailList
            else:
                return []
        else:
            print('----NOT CA----')
            return[]