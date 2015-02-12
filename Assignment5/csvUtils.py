from io import open
from fetchArtist import *
from fetchAlbums import *


def writeArtistsTable(artist_info_list):
    f = open('artists.csv', 'w', encoding = 'utf-8')
    f.write(u'ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY\n')
    #artist_info_list = [artist_info_list]

    for key in artist_info_list:


        f.write(key['id'] + ',' + '"' + key['name'] + '"' + ',' + str(key['followers']) + ',' + str(key['popularity']) + "\n")

    f.close()




def writeAlbumsTable(album_info_list):
    f = open('albums.csv', 'w', encoding = 'utf-8')
    f.write(u'ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY\n')
    #album_info_list = [album_info_list]
    for key in album_info_list:

        f.write(key['artist_id'] + ',' + key['album_id'] + ',' + '"' + key['name'] + '"' + ',' + str(key['year']) + ',' + str(key['popularity'])+"\n")

    f.close()


#artist = fetchArtistInfo('7hJcb9fa4alzcOq3EaNPoG')
#album = fetchAlbumInfo('4ljkpJtSPvuLmOqi4n1YRT')

#writeArtistsTable(artist)
#writeAlbumsTable(album)
