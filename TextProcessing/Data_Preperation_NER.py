# with open('trainingData.txt','w') as writer:
import sqlite3
import pickle

TRAIN_DATA=[]

def pickleList():
    filename = 'training_data'
    outfile = open(filename,'wb')
    pickle.dump(TRAIN_DATA,outfile)
    outfile.close()

def processData(content,category):
    startIndex=content.find(category)
    endIndex=startIndex+len(category)
    TRAIN_DATA.append((content,{"entities": [(startIndex,endIndex,"CA_TYPE")]}))
    # print(content)
    # print(content[startIndex:endIndex])
    # print(category)
    # print(startIndex,' ',endIndex)
    # print()

def readDataFromDb():
    conn=sqlite3.connect('news.db')
    c=conn.cursor()
    c.execute('SELECT * FROM ca_news WHERE category != "null"')
    for row in c:
        processData(row[0],row[1])

if __name__=="__main__":
    readDataFromDb()
    pickleList()