from flask import Flask, render_template, request, redirect, url_for
import pymysql
import pandas as pd
import numpy as np
import networkx as nx
import random
from artistNetworks import *
from analyzeNetworks import *
from fetchArtist import *
from fetchAlbums import *
from io import open
import requests

dbname="playlists"
host="localhost"
user="root"
passwd="Fanficfan2"
db=pymysql.connect(db=dbname, host='127.0.0.1', user=user,passwd=passwd, charset='utf8')
cur = db.cursor()

app = Flask(__name__)


@app.route('/')
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    return(render_template('index.html'))


@app.route('/playlists/')
def make_playlists_resp():
    cur = db.cursor()
    sql = """SELECT Id, rootArtist FROM playlists"""
    cur.execute(sql)
    playlists = []
    for name in cur.fetchall():
        playlists.append(name)

    return render_template('playlists.html',playlists=playlists)


@app.route('/playlist/<playlistId>')
def make_playlist_resp(playlistId):
    cur = db.cursor()
    sql = """SELECT songOrder, artistName, albumName, trackName FROM songs WHERE playlistId = '%s' """ % (playlistId)
    cur.execute(sql)
    songs = []
    for song in cur.fetchall():
        songs.append(song)
    return render_template('playlist.html',songs=songs)


@app.route('/addPlaylist/',methods=['GET','POST'])
def add_playlist():
    if request.method == 'GET':
        # This code executes when someone visits the page.
        return(render_template('addPlaylist.html'))
    elif request.method == 'POST':
        # this code executes when someone fills out the form
        artistName = request.form['artistName']
        createNewPlaylist(artistName)
        return(redirect("/playlists/"))



def createNewPlaylist(name):
    playlist_ids = []
    order = 1
    artist = str(name)
    cur.execute('CREATE TABLE IF NOT EXISTS playlists (Id INTEGER PRIMARY KEY AUTO_INCREMENT, rootArtist VARCHAR(255))')
    cur.execute('CREATE TABLE IF NOT EXISTS songs (playlistId INTEGER, songOrder INTEGER, artistName VARCHAR(255), albumName VARCHAR(255), trackName VARCHAR(255))')

    root_insert = """INSERT INTO playlists (rootArtist) VALUES ('%s')""" % (artist)
    cur.execute(root_insert)

    root_id_select = """SELECT Id FROM playlists WHERE rootArtist = '%s' """ % (artist)
    cur.execute(root_id_select)
    for item in cur.fetchone():
        playlist_id = item
    db.commit()

    artist_id = fetchArtistId(name)
    edge_list = getEdgeList(artist_id, 2)
    final_edge_list = pd.DataFrame.drop_duplicates(edge_list)
    diGraph = pandasToNetworkX(final_edge_list)
    limit = 30
    while limit > 0:
        random_selection = randomCentralNode(diGraph)
        album_list = fetchAlbumIds(random_selection)
        if album_list == []:
            pass
        else:
            playlist_ids.append(random_selection)
            limit = limit-1


    for artist_id in playlist_ids:
        tracks_list = []
        album_list = fetchAlbumIds(artist_id)
        random_album = random.choice(album_list)


        album_url = 'https://api.spotify.com/v1/albums/' + random_album
        req_album = requests.get(album_url)
        album_data = req_album.json()
        album_name = '"' + album_data['name'] + '"'
        album_name = album_name.replace("'",'')
        artist_name = '"' + album_data['artists'][0]['name'] + '"'
        artist_name = artist_name.replace("'",'')



        tracks_url = 'https://api.spotify.com/v1/albums/' + random_album + '/tracks'
        req_tracks = requests.get(tracks_url)
        tracks_data = req_tracks.json()
        tracks_info = tracks_data['items']
        for info in tracks_info:
            track_id = info['id']
            tracks_list.append(track_id)
        random_track = random.choice(tracks_list)


        random_track_url = 'https://api.spotify.com/v1/tracks/' + random_track
        req = requests.get(random_track_url)
        data = req.json()
        track_name = '"' + data['name'] + '"'
        track_name = track_name.replace("'",'')



        songs_insert = """INSERT INTO songs (playlistId, songOrder, artistName, albumName, trackName) VALUES ('%s', '%s', '%s', '%s', '%s');""" % (playlist_id, order, artist_name, album_name, track_name)
        cur.execute(songs_insert)
        db.commit()
        order = order +1


# XXX test - mcc
#createNewPlaylist('Snoop Dogg')
#createNewPlaylist('Avril Lavigne')
#createNewPlaylist('Charlie Parker')
#createNewPlaylist('Orson')
#createNewPlaylist('AC/DC')
#createNewPlaylist('50 Cents')
if __name__ == '__main__':
    app.debug=True
    app.run()
