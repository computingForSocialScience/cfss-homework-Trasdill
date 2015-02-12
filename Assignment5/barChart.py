import unicodecsv as csv
import matplotlib.pyplot as plt

def getBarChartData():
#opens the files artists.csv and albums.csv.
    f_artists = open('artists.csv')
    f_albums = open('albums.csv')

#reads through the various rows in both files and places them in separate variables.
    artists_rows = csv.reader(f_artists)
    albums_rows = csv.reader(f_albums)

#isolates the header for both files.
    artists_header = artists_rows.next()
    albums_header = albums_rows.next()

#creates an empty list 'artist_names'.
    artist_names = []
#sets the range 'decades' from 1900 to 2020 with increments of 10.
    decades = range(1900,2020, 10)
#creates an empty dictionary 'decades_dict'
    decade_dict = {}
#Loops through each 'decade' increment of the 'decades' range and creates a key for it in 'decades_dict' with the value set to 0.
    for decade in decades:
        decade_dict[decade] = 0
#checks if any row in artist_rows is empty (false) and if so, skips it.
    for artist_row in artists_rows:
        if not artist_row:
            continue
#separates each element of the artist_row line into separate elements and appends the 'name' element to the 'artist_names' list
        artist_id,name,followers, popularity = artist_row
        artist_names.append(name)
#checks if any row in album_rows is empty (false) and if so, skips it.
    for album_row  in albums_rows:
        if not album_row:
            continue
#separates each element of the album_row line into separate elements.
        artist_id, album_id, album_name, year, popularity = album_row
#loops through each increment of the 'decades' range. If the previously identified 'year' is both superior or equal to the 'decade' value and inferior to the that value+10,
#the value of that 'decade' key in the 'decade_dict' dictionary is raised by one and the loop breaks.
        for decade in decades:
            if (int(year) >= int(decade)) and (int(year) < (int(decade) + 10)):
                decade_dict[decade] += 1
                break

#defines the values 'x' equal to the 'decades' range and 'y' equal to a list of values from 'decades_dict' for each key 'd' in 'decades'.
    x_values = decades
    y_values = [decade_dict[d] for d in decades]
    return x_values, y_values, artist_names

#Defines the function plotBarChart, which takes no argument.
def plotBarChart():
#Defines the variables x_vals, y_vals and artist_names as equal to the values returned by the getBarChart function.
    x_vals, y_vals, artist_names = getBarChartData()
#Defines a bar chart with
    fig , ax = plt.subplots(1,1)
#Sets the values of the x-axis and y-axis as x_vals and y_vals respectively,
    ax.bar(x_vals, y_vals, width=10)
#Sets the labels for the x-axis and y-axis as well as the title
    ax.set_xlabel('decades')
    ax.set_ylabel('number of albums')
    ax.set_title('Totals for ' + ', '.join(artist_names))
#Displays the bar chart.
    plt.show()
