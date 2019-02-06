import sqlite3
from myCrawler import *


if __name__ == "__main__":
    #подлкючимся к БД и создадим табличку
    conn = sqlite3.connect(r'C:\Users\17060903\Desktop\WorkProjects\MailRuCrawler\MailRuQ&A.db',
                           timeout=10)

    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS data(
                    'q_id' INTEGER,
                    'title' TEXT,
                    'category'TEXT,
                    'subcategory' TEXT,
                    'comment'TEXT,
                    'answer'  TEXT);
                   """)

    #code
    crawler = myCrawler()
    generatorData = crawler.fetchPages(442308,700000)
    crawler.downloadPages(generatorData, cursor, conn)