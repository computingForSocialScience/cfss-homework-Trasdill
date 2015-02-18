import requests
from datetime import datetime

def fetchAlbumIds(artist_id):
    url = 'https://api.spotify.com/v1/artists/' + artist_id + '/albums?market=US&album_type=album'
    req = requests.get(url)
    Album_List = []
    if req.ok == False:
        print 'False Artist Id'
    else:
        data = req.json()
        Album_Data = data['items']
        for item in Album_Data:
            Album_Name = item['id']
            Album_List.append(Album_Name)
    return Album_List


def fetchAlbumInfo(album_id):
    url = 'https://api.spotify.com/v1/albums/' + album_id
    req = requests.get(url)
    if req.ok == False:
        print 'False Artist Id'
    else:
        data = req.json()
        artist_id = data['artists'][0]['id']
        name = data['name']
        year = data['release_date'][:4]
        popularity = data['popularity']
        Album_Info = {'artist_id':artist_id, 'album_id':unicode(album_id), 'name':name, 'year':unicode(year), 'popularity':popularity}
    return Album_Info




# print fetchAlbumIds('7hJcb9fa4alzcOq3EaNPoG')
#print fetchAlbumInfo('24geHauG3JIbpyf9CRiuvf')
