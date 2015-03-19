#Integration#
import sys
from article_data import *
from reference_data import *
from db_manager import *

#Data Storage#
#import csv
from io import open
from flask import Flask, render_template, request, redirect, url_for
import pymysql


##################################


dbname="Final_Project"
host="localhost"
user="root"
passwd="Fanficfan2"
db=pymysql.connect(db=dbname, host="127.0.0.1", user=user,passwd=passwd, charset="utf8")
apikey = "dbaf0b9a837d9c11ab2c5f3d09973d54"


##################################


def coordinator(arguments, size):

    c = db.cursor()

    c.execute("DROP TABLE IF EXISTS article_data")
    c.execute("DROP TABLE IF EXISTS authors")
    c.execute("DROP TABLE IF EXISTS reference_data")
    c.execute("DROP TABLE IF EXISTS reference_authors")
    c.execute("DROP TABLE IF EXISTS recommended_articles")
    c.execute("DROP TABLE IF EXISTS recommended_authors")
    c.execute("DROP TABLE IF EXISTS keywords")
    db.commit()

    c.execute("CREATE TABLE IF NOT EXISTS article_data (Id INTEGER PRIMARY KEY AUTO_INCREMENT, Pub_Year VARCHAR(10), Publication VARCHAR(255), Category VARCHAR(255), Pub_Type VARCHAR(255), Pub_Volume VARCHAR(10), Pub_Number VARCHAR(10), Pages VARCHAR(10), Citation_Count VARCHAR(10), Pii VARCHAR(20), Weburl VARCHAR(255))")
    c.execute("CREATE TABLE IF NOT EXISTS authors (Article_Id INTEGER, Authors VARCHAR(255))")
    c.execute("CREATE TABLE IF NOT EXISTS reference_data (Citing_Id VARCHAR(10), Article_Id INTEGER PRIMARY KEY AUTO_INCREMENT, Status VARCHAR(50), Pub_Year VARCHAR(10), Publication VARCHAR(255), Category VARCHAR(255), Pub_Type VARCHAR(255), Pub_Volume VARCHAR(10), Pub_Number VARCHAR(10), Pages VARCHAR(10), Citation_Count VARCHAR(10), Pii VARCHAR(20), Weburl VARCHAR(255))")
    c.execute("CREATE TABLE IF NOT EXISTS reference_authors (Citing_Id VARCHAR(10), Article_Id INTEGER, Authors VARCHAR(255))")
    c.execute("CREATE TABLE IF NOT EXISTS recommended_articles (Citing_Id VARCHAR(10), Article_Id INTEGER PRIMARY KEY AUTO_INCREMENT, Pub_Year VARCHAR(10), Publication VARCHAR(255), Category VARCHAR(255), Pub_Type VARCHAR(255), Pub_Volume VARCHAR(10), Pub_Number VARCHAR(10), Pages VARCHAR(10), Citation_Count VARCHAR(10), Pii VARCHAR(20), Weburl VARCHAR(255))")
    c.execute("CREATE TABLE IF NOT EXISTS recommended_authors (Citing_Id VARCHAR(10), Article_Id INTEGER, Authors VARCHAR(255))")
    c.execute("CREATE TABLE IF NOT EXISTS keywords (Key_Words VARCHAR(1000))")
    insert = """INSERT INTO keywords (Key_words) VALUES (%s)"""
    c.execute(insert, arguments)
    db.commit()


    articles_dict = {}
    references_dict = {}
    recommendations_dict = {}
    #references_data = {}
    #recommendations_data = {}
    article_list = get_articles(arguments, size)


    for article in article_list:
        references_data = {}
        recommendations_data = {}
        article_info = get_article_info(article)
        #print article_info

        if article_info == None:
            continue

        else:
            weburl = "http://www.sciencedirect.com/science/article/pii/" + article_info["PII"]

            scrape_info = scrape_webpage(weburl)
            citation_count = scrape_info["CITATION_COUNT"]
            reference_list = scrape_info["REFERENCES"]
            recommendation_list = scrape_info["RECOMMENDATIONS"]
            #print scrape_info["RECOMMENDATIONS"]

            article_id = articles_to_MySQL(article_info, citation_count)

            article_json_prepare = articles_to_json(article_info)
            articles_dict[article_id] = article_json_prepare

            for reference in reference_list:
                reference_info = reference_soup(reference)

                if reference_info == None:
                    continue

                else:
                    reference_id = references_to_MySQL(reference_info, article_id)
                    reference_json_prepare = references_to_json(reference_info)
                    references_data[reference_id] = reference_json_prepare


            for recommendation in recommendation_list:
                recommendation_info = get_article_info(recommendation)

                if recommendation_info == None:
                    continue

                else:
                    recommendation_link = "http://www.sciencedirect.com/science/article/pii/" + str(recommendation)
                    recommendation_scrape = scrape_webpage(recommendation_link)
                    recommendation_citation_count = recommendation_scrape["CITATION_COUNT"]
                    recommendation_id = recommendations_to_MySQL(recommendation_info, recommendation_citation_count, article_id)
                    recommendation_json_prepare = recommendations_to_json(recommendation_info)

                    recommendations_data[recommendation_id] = recommendation_json_prepare

        references_dict[article_id] = references_data
        recommendations_dict[article_id] = recommendations_data

    article_json = json.dumps(articles_dict, sort_keys=True, indent=4, separators=(",", ": "))
    json_article = unicode(article_json)
    articles = open("articles.json", "w", encoding = 'utf-8')
    articles.write(json_article)
    articles.close()


    reference_json = json.dumps(references_dict, sort_keys=True, indent=4, separators=(",", ": "))
    json_reference = unicode(reference_json)
    references = open("references.json", "w", encoding = 'utf-8')
    references.write(json_reference)
    references.close()


    recommendation_json = json.dumps(recommendations_dict, sort_keys=True, indent=4, separators=(",", ": "))
    json_recommendation = unicode(recommendation_json)
    recommendations = open("recommendations.json", "w", encoding = 'utf-8')
    recommendations.write(json_recommendation)
    recommendations.close()


##################################


#test#
#coordinator("Heart Attack", 2)
#articles = open('articles.json', 'r')
#print json.load(articles)
