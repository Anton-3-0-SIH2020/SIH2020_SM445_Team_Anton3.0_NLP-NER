# with open('trainingData.txt','w') as writer:
import sqlite3
import pickle

TRAIN_DATA=[]

def pickleList():
    filename = 'training_data'
    outfile = open(filename,'wb')
    pickle.dump(TRAIN_DATA,outfile)
    outfile.close()

def processData(content,category,purpose):
    startIndexCategory=content.find(category)
    endIndexCategory=startIndexCategory+len(category)

    startIndexPurpose=content.find(purpose)
    endIndexPurpose=startIndexPurpose+len(purpose)

    if purpose=='null':
        TRAIN_DATA.append((content,{"entities": [(startIndexCategory,endIndexCategory,"CA_TYPE")]}))
    else:
        TRAIN_DATA.append((content,{"entities": [(startIndexCategory,endIndexCategory,"CA_TYPE"),(startIndexPurpose,endIndexPurpose,"PURPOSE")]}))
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
        processData(row[0],row[1],row[2])

if __name__=="__main__":
    readDataFromDb()
    pickleList()