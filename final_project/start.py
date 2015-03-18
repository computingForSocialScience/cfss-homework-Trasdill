from flask import Flask, render_template, request, redirect, url_for
import pymysql
from io import open
import requests
import json
from main import *
from pretty_plots import *

dbname="final_project"
host="localhost"
user="root"
passwd="Fanficfan2"
db=pymysql.connect(db=dbname, host='127.0.0.1', user=user,passwd=passwd, charset='utf8')
c = db.cursor()

app = Flask(__name__)


@app.route('/')
def present():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    return(render_template('index.html'))


@app.route('/kitchen/',methods=['GET','POST'])
def cook():
    if request.method == 'GET':

        return(render_template('kitchen.html'))
    elif request.method == 'POST':

        key_words = request.form['keyWords']
        input_size = request.form['inputSize']
        coordinator(key_words, input_size)

        return(redirect("/bowl/"))


@app.route('/bowl/')
def serve():
    c = db.cursor()
    sql = """SELECT Key_Words FROM keywords"""
    c.execute(sql)
    arguments = str(c.fetchone())[3:-3]

    return render_template('bowl.html', arguments=arguments)


@app.route('/broth/')
def stir():
    f = open('articles.json', 'r')
    loading = json.load(f)

    return(render_template('broth.html', articles=loading))


@app.route('/broth/<articleId>')
def swirl(articleId):
    f = open('articles.json', 'r')
    art_load = json.load(f)
    main_article = art_load[articleId]
    f.close()

    g = open('references.json', 'r')
    ref_load = json.load(g)
    ref_articles = ref_load[articleId]
    g.close()

    h = open('recommendations.json', 'r')
    rec_load = json.load(h)
    rec_articles = rec_load[articleId]
    h.close()


    c = db.cursor()

    art_sql = """SELECT Citation_Count,Weburl FROM article_data WHERE Id=%s""" % (articleId)
    c.execute(art_sql)
    article_data = []
    for things in c.fetchall():
        article_data.append(things)

    ref_sql = """SELECT Article_Id, Citation_Count,Weburl FROM reference_data WHERE Citing_Id=%s AND Status='Available via Elsevier' OR Citing_id=%s AND status='Available via External Link'""" % (articleId,articleId)
    c.execute(ref_sql)
    reference_data = []
    for things in c.fetchall():
        reference_data.append(things)
    ref_identifier = {}
    for ids, citation, weburl in reference_data:
        ref_identifier[ids] = unicode(ids)


    rec_sql = """SELECT Article_Id, Citation_Count,Weburl FROM recommended_articles WHERE Citing_Id=%s""" % (articleId)
    c.execute(rec_sql)
    recommendation_data = []
    for things in c.fetchall():
        recommendation_data.append(things)
    rec_identifier = {}
    for ids, citation, weburl in recommendation_data:
        rec_identifier[ids] = unicode(ids)

    return(render_template('bouillon.html', ref_identifier=ref_identifier, rec_identifier=rec_identifier, main_article=main_article, ref_articles=ref_articles, rec_articles=rec_articles, article_data=article_data, reference_data=reference_data, recommendation_data=recommendation_data))


@app.route('/croutons/')
def bread():
    authors = author_table()
    journal_table()
    availability()
    year_chart()
    category_chart()
    counts_histogram()

    return(render_template('croutons.html', authors=authors))
    #, journals=journals, availability=availability, year_chart=year_chart, category_chart=category_chart, counts_histogram=counts_histogram




# XXX test - mcc
if __name__ == '__main__':
    app.debug=True
    app.run()
