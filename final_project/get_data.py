import sys
import requests
from io import open


dbname="Final_Project"
host="localhost"
user="root"
passwd="Fanficfan2"
db=pymysql.connect(db=dbname, host='127.0.0.1', user=user,passwd=passwd, charset='utf8')
apikey = 'dbaf0b9a837d9c11ab2c5f3d09973d54'


def get_article_info(DOI):

    article_data ={}
    #url = 'http://api.elsevier.com/content/article/' + DOI + '?httpAccept=application/json&APIKey=' + apikey
    #test URL with API Key directly included:
    url = 'http://api.elsevier.com/content/article/' + DOI + '?httpAccept=application/json&APIKey=dbaf0b9a837d9c11ab2c5f3d09973d54'


    #print url
    req = requests.get(url)
    if req.ok == False:
        #print 'False Input'
        article_data = None

    else:
        data = req.json()
        get_info = data['full-text-retrieval-response']['coredata']
        authors = []
        urls = []
        name_data = get_info['dc:creator']
        if type(name_data) is list:

            for name in name_data:
                author = name['$']
                authors.append(author)

        else:

            authors.append(name_data)

        weburl = get_info['link'][1]['@href']

        date = get_info['prism:coverDate']
        title = get_info['dc:title']
        publication = get_info['prism:publicationName']
        publication_type = get_info['prism:aggregationType']
        if 'prism:volume' not in get_info:
            volume = 'None'
        else:
            volume = get_info['prism:volume']
        if 'prism:issueIdentifier' not in get_info:
            number = 'None'
        else:
            number =  get_info['prism:issueIdentifier']
        if 'prism:startingPage' not in get_info:
            pages = ''
        elif 'prism:endingPage' not in get_info:
            pages = get_info['prism:startingPage']
        else:
            pages =  get_info['prism:startingPage'] + '-' +  get_info['prism:endingPage']
        description = get_info['dc:description']

        article_data = {'AUTHORS':authors,'DATE':date,'TITLE':title,'PUBLICATION':publication,'TYPE':publication_type,'VOLUME':volume,'NUMBER':number,'PAGES':pages,'DESCRIPTION':description,'WEBURL':weburl,'APIURL':url}
        #testing without descriptions:
        #article_data = {'AUTHORS':authors,'DATE':date,'TITLE':title,'PUBLICATION':publication,'TYPE':publication_type,'VOLUME':volume,'NUMBER':number,'PAGES':pages}

    return article_data



def write_to_csv(info_list):

    if info_list == None:
        return

    else:
        mystr = '%s, (%s) , "%s" , %s , (%s) , %s , %s , %s , "%s", %s, %s\n' % (info_list['AUTHORS'], info_list['DATE'], info_list['TITLE'],info_list['PUBLICATION'], info_list['TYPE'] , info_list['VOLUME'],  info_list['NUMBER'],  info_list['PAGES'], info_list['DESCRIPTION'],
        info_list['APIURL'], info_list['WEBURL'])
        #testing without descriptions:
        #mystr = '%s, (%s) , "%s" , %s , (%s) , %s , %s , %s\n' % (info_list['AUTHORS'], info_list['DATE'], info_list['TITLE'],info_list['PUBLICATION'], info_list['TYPE'] , info_list['VOLUME'],  info_list['NUMBER'],  info_list['PAGES'])
        #url = '%s, %s\n' % (info_list['APIURL'], info_list['WEBURL'])
        articles.write(mystr)
        #urls.write(url)



def add_to_MySQL(info_list):

    if info_list == None:
        return

    else:
        data_insert = """INSERT INTO article_data (Authors, Pub_Date, Title, Publication, Pub_Type, Pub_Volume, Pub_Number, Pages, API_url, Web_url, Description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""" % (info_list['AUTHORS'], info_list['DATE'], info_list['TITLE'],info_list['PUBLICATION'], info_list['TYPE'] , info_list['VOLUME'],  info_list['NUMBER'],  info_list['PAGES'],
        info_list['APIURL'], info_list['WEBURL'], info_list['DESCRIPTION'])

        c.execute(data_insert)
        db.commit()




def get_articles(arguments):
    #url = 'http://api.elsevier.com/content/search/index:SCIDIR?query=' + arguments + '&APIKey=' + apikey + '&httpAccept=application/json&count=200'
    #test URL with API Key directly included:
    url = 'http://api.elsevier.com/content/search/index:SCIDIR?query=' + arguments + '&APIKey=dbaf0b9a837d9c11ab2c5f3d09973d54&httpAccept=application/json&count=200'
#    print url
    DOI_list = []
    req = requests.get(url)
    if req.ok == False:
        print 'False Input'
    else:
        data = req.json()
        get_results = data['search-results']['entry']
        check = data['search-results']
        if check['opensearch:totalResults'] == None:
            print 'Error: No Results'
        else:
            for item in get_results:
                DOI = item['dc:identifier']
                DOI_list.append(DOI)

    for DOI in DOI_list:
        data = get_article_info(DOI)
#        writing = write_to_csv(data)
        writing = add_to_MySQL(data)


#testing
#print get_article_info('DOI:10.1016/j.amjcard.2014.12.033')
#print get_article_info('DOI:10.1016/j.jhealeco.2012.04.004')
#Web of Science Sign-in PW: IAmTrasdill*3

if __name__ == "__main__":
    arguments = str(sys.argv[1:])

#MySQL Indexing:
    c = db.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS article_data (Id INTEGER PRIMARY KEY AUTO_INCREMENT, Authors VARCHAR(255), Pub_Date DATE, Title VARCHAR(255), Publication VARCHAR(255), Pub_Type VARCHAR(255), Pub_Volume VARCHAR(255), Pub_Number VARCHAR(255), Pages VARCHAR(255), API_url VARCHAR(255), Web_url VARCHAR(255), Description TEXT)')
    get_articles(arguments)
    db.commit()
#CSV Writing:
#    articles = open('articles.csv', 'w', encoding = 'utf-8')
    #urls = open('urls.csv', 'w', encoding = 'utf-8')
#    articles.write(u'AUTHORS,DATE,TITLE,PUBLICATION,TYPE,VOLUME,NUMBER,PAGES,DESCRIPTION,API_URL,WEB_URL\n')
    #urls.write(u'API_URL,WEB_URL\n')
#    get_articles(arguments)
    #var = raw_input("please enter: ")
    #print "you entered", var
#    articles.close()
    #urls.close()
