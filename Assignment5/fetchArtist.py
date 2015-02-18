import sys
import requests
import csv

def fetchArtistId(name):
    url = 'https://api.spotify.com/v1/search?q=' + name + '&type=artist'
    req = requests.get(url)
    if req.ok == False:
        print 'False Artist Name'
    else:
        data = req.json()
        Artist_ID = data['artists']['items'][0]['id']
    return Artist_ID


def fetchArtistInfo(artist_id):
    url = 'https://api.spotify.com/v1/artists/' + artist_id
    req = requests.get(url)
    if req.ok == False:
        print 'False Artist Id'
    else:
        data = req.json()
        followers = data['followers']['total']
        genres = data['genres']
        name = data['name']
        popularity = data['popularity']
    Artist_Info = {'name':name, 'genres':genres, 'popularity':unicode(popularity), 'followers':unicode(followers), 'id':unicode(artist_id)}
    return Artist_Info


print fetchArtistId('Avril Lavigne')
#print fetchArtistInfo('7hJcb9fa4alzcOq3EaNPoG')
