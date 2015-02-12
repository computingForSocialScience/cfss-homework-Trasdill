import sys
from fetchArtist import fetchArtistId, fetchArtistInfo
from fetchAlbums import fetchAlbumIds, fetchAlbumInfo
from csvUtils import writeArtistsTable, writeAlbumsTable
from barChart import plotBarChart

if __name__ == '__main__':
    artist_names = sys.argv[1:]
    print "input artists are ", artist_names
    artist_id = []
    album_id = []

    artist_info = [fetchArtistInfo(fetchArtistId(i)) for i in artist_names]
    album_info = []
    for i in artist_info:
        for item in fetchAlbumIds(i['id']):
            album_info.append(fetchAlbumInfo(item))
    writeArtistsTable(artist_info)
    writeAlbumsTable(album_info)
    plotBarChart()
