from NewsScraper import Money_Control_Scraper
import sqlite3
import csv
import spacy
import pickle
import en_core_web_sm




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

if __name__=="__main__":
    # initializeDb()
    # moneyControlScraper=Money_Control_Scraper.MoneyControlScraper()
    # moneyControlScraper.scrapeNews()
    # writeDataInCsv()
    # createDbOfCaForNer()

    news='Va Tech Wabag is quoting ex-split today. The company approved a proposal to sub-divide each ordinary equity share of face value of Rs 5/- each into face value of Rs 2 each fully paid up on May 26, 2011. The record date has been fixed at August 17.'
    getGeneralDetails(news)
    getCaType(news)