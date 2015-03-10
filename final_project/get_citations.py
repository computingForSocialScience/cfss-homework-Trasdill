import sys
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from io import open
from get_data import *

dbname="Final_Project"
host="localhost"
user="root"
passwd="Fanficfan2"
db=pymysql.connect(db=dbname, host='127.0.0.1', user=user,passwd=passwd, charset='utf8')
c = db.cursor()
apikey = 'dbaf0b9a837d9c11ab2c5f3d09973d54'

def get_article_urls():
    urls_extract = """SELECT Web_url FROM article_data"""
    c.execute(urls_extract)
    url_list = []
    for url in cur.fetchall():





def fetch_citations(csv_file)

url =
req = requests.get(url)
src = req.text
soup = bs(src)


#retrieves citations for articles
#reconfigure for MySQL instead of csv
