import csv
import sys

def readCSV(filename):
    '''Reads the CSV file `filename` and returns a list
    with as many items as the CSV has rows. Each list item
    is a tuple containing the columns in that row as strings.
    Note that if the CSV has a header, it will be the first
    item in the list.'''
    with open(filename,'r') as f:
        rdr = csv.reader(f)
        lines = list(rdr)
    return(lines)


def get_avg_latlng(filename):
    lat = []
    lng = []
    first = True
    for item in readCSV(filename):
        if (first == True):
            first = False
            continue
        if (item[-3] == ''):
            continue
        if (item[-2] == ''):
            continue
        latint = float(item[-3])
        lngint = float(item[-2])
        lat.append(latint)
        lng.append(lngint)
    avg_lat = sum(lat)/len(lat)
    avg_lng = sum(lng)/len(lng)
    print avg_lat
    print avg_lng


from matplotlib import pyplot as plt
def zip_code_barchart(filename):
    first = True
    zipdata = []
    for item in readCSV(filename):
        if (first == True):
            first = False
            continue
        zipdata.append(item[28])
        zipdata.append(item[35])
        zipdata.append(item[42])
        zipdata.append(item[49])
        zipdata.append(item[56])
        zipdata.append(item[63])
        zipdata.append(item[70])
        zipdata.append(item[77])
        zipdata.append(item[84])
        zipdata.append(item[91])
        zipdata.append(item[98])
        zipdata.append(item[105])
        zipdata.append(item[112])
        zipdata.append(item[119])
        zipdata.append(item[126])

    zipstring= []
    for i in range(0, len(zipdata)):
        if zipdata[i] != '':
            zipstring.append(zipdata[i])

    ziplist = []
    for code in zipstring:
        zipcode = code[0:5]
        ziplist.append(int(zipcode))


    plt.hist(ziplist, bins=200)
    plt.savefig('zipcode_histogram.jpg')


if sys.argv[1] == 'latlong':
    get_avg_latlng('permits_hydepark.csv')
elif sys.argv[1] == 'hist':
    zip_code_barchart('permits_hydepark.csv')
