#Data Encoding and Storage#
import csv
import json
import pymysql


##################################


dbname="Final_Project"
host="localhost"
user="root"
passwd="Fanficfan2"
db=pymysql.connect(db=dbname, host="127.0.0.1", user=user,passwd=passwd, charset="utf8")
c = db.cursor()


##################################


def articles_to_MySQL(info_dict,citation_count):

    if info_dict == None:
        return

    else:
        data_insert = """INSERT INTO article_data (Pub_Year, Publication, Category, Pub_Type, Pub_Volume, Pub_Number, Pages, Citation_Count, Pii, Weburl)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        c.execute(data_insert, (info_dict["YEAR"], info_dict["PUBLICATION"], info_dict["CATEGORY"], info_dict["TYPE"] , info_dict["VOLUME"],  info_dict["NUMBER"],
         info_dict["PAGES"], citation_count, info_dict["PII"], info_dict["WEBURL"]))
        db.commit()

        #get_id = """SELECT Id from article_data WHERE Title = atitle """
        #c.execute("""SELECT Id from article_data WHERE Title = %s """, atitle)
        article_id = c.lastrowid
        #print article_id

        authors = info_dict["AUTHORS"]
        for author in authors:
            author_insert = """INSERT INTO authors (Article_Id, Authors) VALUES (%s, %s)"""
            c.execute(author_insert, (article_id, author))
            db.commit()

        return str(article_id)


def references_to_MySQL(info_dict,article_id):

    if info_dict == None:
        return

    else:
        data_insert = """INSERT INTO reference_data (Citing_Id, Status, Pub_Year, Publication, Category, Pub_Type, Pub_Volume, Pub_Number, Pages, Citation_Count, Pii, Weburl)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        c.execute(data_insert, (article_id, info_dict["AVAILABILITY"], info_dict["YEAR"], info_dict["PUBLICATION"], info_dict["CATEGORY"], info_dict["TYPE"], info_dict["VOLUME"],
        info_dict["NUMBER"], info_dict["PAGES"], info_dict["CITATION_COUNT"], info_dict["PII"], info_dict["WEBURL"]))
        db.commit()

        reference_id = c.lastrowid

        authors = info_dict["AUTHORS"]
        for author in authors:
            author_insert = """INSERT INTO reference_authors (Citing_Id, Article_Id, Authors) VALUES (%s, %s, %s)"""
            c.execute(author_insert, (article_id, reference_id, author))
            db.commit()

        return str(reference_id)


def recommendations_to_MySQL(info_dict,citation_count,article_id):

    if info_dict == None:
        return

    else:
        data_insert = """INSERT INTO recommended_articles (Citing_Id, Pub_Year, Publication, Category, Pub_Type, Pub_Volume, Pub_Number, Pages, Citation_Count, Pii, Weburl)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        c.execute(data_insert, (article_id, info_dict["YEAR"], info_dict["PUBLICATION"], info_dict["CATEGORY"], info_dict["TYPE"], info_dict["VOLUME"], info_dict["NUMBER"],
        info_dict["PAGES"], citation_count, info_dict["PII"], info_dict["WEBURL"]))
        db.commit()

        recommendation_id = c.lastrowid

        authors = info_dict["AUTHORS"]
        for author in authors:
            author_insert = """INSERT INTO recommended_authors (Citing_Id, Article_Id, Authors) VALUES (%s, %s, %s)"""
            c.execute(author_insert, (article_id, recommendation_id, author))
            db.commit()

    return str(recommendation_id)

def articles_to_json(info_dict):

    if info_dict == None:
        return

    else:
        data = {"TITLE":info_dict["TITLE"], "DESCRIPTION":info_dict["DESCRIPTION"], "FULL_TEXT":info_dict["FULL_TEXT"]}

        return data


def references_to_json(info_dict):

    if info_dict == None:
        return

    else:
        data = {"TITLE":info_dict["TITLE"], "DESCRIPTION":info_dict["DESCRIPTION"], "FULL_TEXT":info_dict["FULL_TEXT"]}

        return data


def recommendations_to_json(info_dict):

    if info_dict == None:
        return

    else:
        #data = {"TITLE":info_dict["TITLE"], "DESCRIPTION":info_dict["DESCRIPTION"], "FULL_TEXT":info_dict["FULL_TEXT"]}
        data = {"TITLE":info_dict["TITLE"]}

        return data
