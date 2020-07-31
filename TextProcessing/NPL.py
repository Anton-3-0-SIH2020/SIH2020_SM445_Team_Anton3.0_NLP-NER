import spacy
import pickle
import en_core_web_sm

def getCaType(news):
    nlp=spacy.load('nlp_model')
    doc = nlp('FedEx has announced the issuance of bonus shares in the first quarter of FedEx from Rs 10 each into 2 equity shares of Rs 10/- each into equity shares of Rs 10 each for every one existing fully paid - up on October 5 , 2011.Innovative Tech Pack is quoting ex - bonus today .')
    for ent in doc.ents:
        print('CA Type: '+ent.text)


def getGeneralDetails(news):
    org=''
    ex_date=''
    record_date=''

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(news)
    for ent in doc.ents:
        if(ent.label_=='ORG' and org==''):
            org=ent.text
        elif(ent.label_=='DATE' and ex_date==''):
            ex_date=ent.text
        elif(ent.label_=='DATE' and record_date==''):
            record_date=ent.text

    print('Organisation: '+org)
    print('Ex-Date: '+ex_date)
    print('Record-Date: '+record_date)
if __name__=='__main__':
    getGeneralDetails("Chevron has approved a proposal to sub - divide each ordinary equity share of the current face value of equity shares of Re 1/- each on September 26 , 2011")
    getCaType("Chevron has approved a proposal to sub - divide each ordinary equity share of the current face value of equity shares of Re 1/- each on September 26 , 2011")