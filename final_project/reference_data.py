#Integration#
from article_data import *

#Data Collection#
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import re
import time


##################################


def scrape_webpage(url):

    all_data = {}
    #wd = webdriver.Firefox()
    wd = webdriver.PhantomJS("C:/phantomjs-2.0.0-windows/bin/phantomjs.exe")
    wd.maximize_window()
    wd.get(url)
    time.sleep(2)
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    html_source = wd.page_source
    soup = bs(html_source)
    wd.quit()

    cite_row = soup.find("span", id="hitcount")
    if cite_row == None:
        citation_count = "0"

    else:
        citation_count = str(cite_row.text)

    ref_rows = soup.find_all("ul", class_= "reference")
    recommend = []
    rec_rows = soup.find_all("a", class_= "cLink S_C_artTitle")

    for row in rec_rows:
        rec_link = row["href"]
        rec_pii = str(rec_link)[21:]
        recommend.append(rec_pii)

    all_data = {"CITATION_COUNT":citation_count, "REFERENCES":ref_rows, "RECOMMENDATIONS":recommend}
    #all_data = {"CITATION_COUNT":citation_count, "RECOMMENDATIONS":recommend}

    return all_data


def reference_soup(soup):

    reference_data = {}

    link_row = soup.find("li", class_= "external refPlaceHolder")

    if link_row == None:
        status = "Unavailable"
        pii = "N/A"
        authors = ["N/A"]
        year = "N/A"
        title = None
        publication = "N/A"
        publication_type = "N/A"
        volume = "N/A"
        number = "N/A"
        pages = "N/A"
        full_text = None
        description = None
        weburl = "N/A"
        citation_count = "N/A"
        category = "N/A"

    else:
        citation_tag = link_row.find("span", class_= "citedBy_")

        if citation_tag == None:
            citation_count = "N/A"

        else:
            citation_text = citation_tag.get_text()
            #print citation_text
            citation_count = str(citation_text)[17:]
            #citation_count = citation_count.replace("(","")
            citation_count = citation_count.replace(")","")
            #print citation_count

        link_tag = link_row.find("a", class_= "cLink")

        if link_tag == None:
            crossref = link_row.find("a", rel = "nofollow")

            if crossref == None:
                status = "Unavailable"
                pii = "N/A"
                authors = ["N/A"]
                year = "N/A"
                title = None
                publication = "N/A"
                publication_type = "N/A"
                volume = "N/A"
                number = "N/A"
                pages = "N/A"
                full_text = None
                description = None
                weburl = "N/A"
                category = "N/A"

            else:
                #cross_tag = crossref.find_parents("a")
                weburl = str(crossref["href"])[7:]
                status = "Available via external Link"
                authors = ["N/A"]
                year = "N/A"
                title = None
                publication = "N/A"
                publication_type = "N/A"
                volume = "N/A"
                number = "N/A"
                pages = "N/A"
                full_text = None
                pii = "N/A"
                description = None
                category = "N/A"

        else:
            link = link_tag["href"]
            pii = str(link)[21:]
            data = get_article_info(pii)

            if data == None:
                status = "Unavailable"
                authors = ["N/A"]
                year = None
                title = "N/A"
                publication = "N/A"
                publication_type = "N/A"
                volume = "N/A"
                number = "N/A"
                pages = "N/A"
                full_text = None
                description = None
                weburl = "N/A"
                category = "N/A"

            else:
                status = "Available via Elsevier"
                authors = data["AUTHORS"]
                year = data["YEAR"]
                title = data["TITLE"]
                publication = data["PUBLICATION"]
                publication_type = data["TYPE"]
                volume = data["VOLUME"]
                number = data["NUMBER"]
                pages = data["PAGES"]
                full_text = data["FULL_TEXT"]
                description = data["DESCRIPTION"]
                weburl = data["WEBURL"]
                category = data["CATEGORY"]


    reference_data = {"CITATION_COUNT":citation_count, "AVAILABILITY":status, "AUTHORS":authors, "YEAR":year,"TITLE":title, "CATEGORY":category, "PUBLICATION":publication,"TYPE":publication_type,"VOLUME":volume,"NUMBER":number,"PAGES":pages,"DESCRIPTION":description,"PII":pii, "WEBURL":weburl, "FULL_TEXT":full_text}

    return reference_data








#testing
#print scrape_webpage("http://www.sciencedirect.com/science/article/pii/S0002914914023157")["RECOMMENDATIONS"]
