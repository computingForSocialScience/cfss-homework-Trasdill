import sys
import requests
from io import open
import random
import pandas as pd
import numpy as np
import networkx as nx
from artistNetworks import *
from analyzeNetworks import *
from fetchArtist import *
from fetchAlbums import *

arguments = sys.argv[1:]
combined_edge_list = []
playlist_ids = []

for artist in arguments:
    artist_id = fetchArtistId(artist)
    edge_list = getEdgeList(artist_id, 2)
    combined_edge_list.append(edge_list)

concatenated_edge_list = pd.concat(combined_edge_list)
final_edge_list = pd.DataFrame.drop_duplicates(concatenated_edge_list)
DiGraph = pandasToNetworkX(final_edge_list)



limit = 30
while limit > 0:
    random_selection = randomCentralNode(DiGraph)
    playlist_ids.append(random_selection)
    limit = limit-1



output = open('playlist.csv', 'w', encoding = 'utf-8')
output.write(u'ARTIST_NAME,ALBUM_NAME,TRACK_NAME\n')
for artist_id in playlist_ids:

    tracks_list = []
    album_list = fetchAlbumIds(artist_id)
    random_album = random.choice(album_list)


    album_url = 'https://api.spotify.com/v1/albums/' + random_album
    req_album = requests.get(album_url)
    album_data = req_album.json()
    album_name = album_data['name']
    artist_name = album_data['artists'][0]['name']


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
    track_name = data['name']


    output.write('"' + artist_name + '"' + ',' + '"' + album_name + '"' + ',' + '"' + track_name + '"' + '\n')

output.close()
#print type(album_list)
