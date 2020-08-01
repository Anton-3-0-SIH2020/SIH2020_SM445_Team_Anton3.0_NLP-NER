import sqlite3

def read_db():
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    c.execute('SELECT * FROM news WHERE category="ca"')
    data = c.fetchall()
    return data


def generate_corpus_text():
    txt = ""
    data = read_db()
    for row in data:
        txt += row[1]
    with open('corpus.txt', 'w') as corpus:
        corpus.write(txt)
