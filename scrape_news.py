import json
from bs4 import BeautifulSoup as bs4
import os
import sqlite3
import requests


class ScrapeIndiaToday:

    def __init__(self):
        self.website = "https://www.indiatoday.in/business?page={}"
        self.page_no = 0
        self.data = []

    def process_text(self, text):
        text = text.replace('\n', ' ')
        text = text.replace('\u2019', "'")
        text = text.replace('\u00a0', ' ')
        text = text.replace('\u00e9', ' ')
        text = text.replace('\u201d', "")
        text = text.replace('\u201c',  "")
        text = text.replace('\u2014', " ")
        text = text.replace('\u2018',  " ")
        text = text.replace('\"',  "")
        text = text.replace('\\',  "")
        text = text.strip()
        return text

    def scrape_page(self, soup):
        content = soup.find(id="content")
        news_list_unprocessed = content.findAll(
            'div', {"class": "catagory-listing"})
        for news in news_list_unprocessed:
            text = news.find('p').getText()
            if text:
                text = self.process_text(text)
                self.data.append({'content': text})

    def get_india_today(self):
        while(self.page_no != 15):
            self.page_no += 1
            res = requests.get(self.website.format(self.page_no))
            soup = bs4(res.content, features='lxml')
            self.scrape_page(soup)
        with open('india_today.json', 'w') as it:
            json.dump(self.data, it, indent=4)

    def dump_in_db(self):
        conn = sqlite3.connect("news.db")
        c = conn.cursor()
        add_data_to_db = "INSERT INTO news VALUES (?,?,?,?)"

        for news in self.data:
            if not news['content']:
                continue
            c.execute(
                add_data_to_db,
                ('Not Present', news["content"],
                'script generated', None),
            )
        conn.commit()
        conn.close()


sc = ScrapeIndiaToday()
sc.get_india_today()
sc.dump_in_db()
