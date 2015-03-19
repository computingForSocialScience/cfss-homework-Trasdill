from flask import Flask, render_template, request, redirect, url_for
import pymysql
from io import open
import requests
import json

dbname="final_project"
host="localhost"
user="root"
passwd="Fanficfan2"
db=pymysql.connect(db=dbname, host='127.0.0.1', user=user,passwd=passwd, charset='utf8')
c = db.cursor()

def test():
    f = open('articles.json', 'r')
    loading = json.load(f)

    keys = sorted(loading.keys(), key=int)

    return keys

print test()
