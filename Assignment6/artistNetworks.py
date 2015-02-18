import sys
import requests
import pandas as pd
import numpy as np


def getRelatedArtists(artist_id):
    url = 'https://api.spotify.com/v1/artists/' + artist_id + '/related-artists'
    req = requests.get(url)
    related_artists = []
    if req.ok == False:
        print 'False Artist ID'
    else:
        data = req.json()
        related_data = data['artists']
        for item in related_data:
            related_id = item['id']
            related_artists.append(related_id)
    return related_artists



def getDepthEdges(artist_id, depth):
    related_artists = getRelatedArtists(artist_id)
    artist_edge = []
    edgelist = []
    for artist in related_artists:
        binome = (artist_id, artist)
        artist_edge.append(binome)

    while depth > 1:
        deep_data = []
        for artist in related_artists:
            deep_relations = getRelatedArtists(artist)
            for deep_artist in deep_relations:
                binome = (artist, deep_artist)
                artist_edge.append(binome)
            deep_data.append(deep_relations)

        related_artists = deep_data
        depth = depth - 1

    for binome in artist_edge:
        if binome not in edgelist:
            edgelist.append(binome)


    return edgelist



def getEdgeList(artist_id, depth):
    edgelist = getDepthEdges(artist_id, depth)
    edgeframe = pd.DataFrame(edgelist)
    return edgeframe



def writeEdgeList(artist_id, depth, filename):
    edgeframe = getEdgeList(artist_id, depth)
    edgeframe.to_csv(filename, index=False)



#for testing the functions
#snoop_dogg = '7hJcb9fa4alzcOq3EaNPoG'
#avril_lavigne = '0p4nmQO2msCgU4IF37Wi3j'
#print getRelatedArtists(snoop_dogg)
#print getRelatedArtists(avril_lavigne)
#print getDepthEdges(snoop_dogg, 2)
#print getEdgeList(snoop_dogg, 2)
#writeEdgeList(snoop_dogg, 2, 'Doggumentary')
#writeEdgeList(avril_lavigne, 2, 'The Best Damn Thing')
