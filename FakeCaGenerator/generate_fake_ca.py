import markovify
import re
import spacy
import random
import json
import os
import sqlite3
import re

nlp = spacy.load("en")


class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


def generate_fake_ca():
    with open("corpus.txt") as f:
        text = f.read()

    with open("company_list.txt", "r") as company:
        companies = company.readlines()

    company_list = []

    for company in companies:
        company_list.append(company.strip())
    text_model = POSifiedText(text)

    json_data = []

    content_size_list = [x for x in range(100, 400)]

    for i in range(300):
        sentence_size = random.randint(0, 199)
        company_name_index = random.randint(0, len(company_list)-1)
        company_name = company_list[company_name_index]
        content = text_model.make_short_sentence(
            content_size_list[sentence_size])
        if not content:
            continue
        headline = company_name
        content = re.sub('the company', company_name,
                         content, flags=re.IGNORECASE)
        link = "script generated"
        category = "ca"
        temp_dict = {
            "headline": headline,
            "content": content,
            "link": link,
            "category": category,
        }
        json_data.append(temp_dict)

    conn = sqlite3.connect("news.db")
    c = conn.cursor()
    add_data_to_db = "INSERT INTO news VALUES (?,?,?,?)"

    for news in json_data:
        if not news['content']:
            continue
        c.execute(
            add_data_to_db,
            (news["headline"], news["content"],
            news["link"], news["category"]),
        )
    conn.commit()
    conn.close()