#Data Collection#
import requests


#For Testing Purposes#
import csv
import json


##################################


apikey = "dbaf0b9a837d9c11ab2c5f3d09973d54"


##################################


def get_article_info(pii):

    article_data ={}
    url = "http://api.elsevier.com/content/article/pii:" + pii + "?httpAccept=application/json&APIKey=" + apikey


    #print url
    req = requests.get(url)
    if req.ok == False:
        #print "False Input"
        article_data = None

    else:
        data = req.json()

        get_data = data["full-text-retrieval-response"]
        get_info = get_data["coredata"]
        authors = []
        urls = []
        name_data = get_info["dc:creator"]

        if type(name_data) is list:

            for name in name_data:
                author = name["$"]
                #author = author.replace("'","")
                authors.append(author)

        else:
            author = name_data
            #author = author.replace("'","")
            authors.append(author)

        weburl = str(get_info["link"][1]["@href"])[7:]

        date = str(get_info["prism:coverDate"])

        year = date[:4]

        title = get_info["dc:title"]
        title = title.replace("'","")

        if "pubType" not in get_info:
            category = "N/A"

        else:
            category = get_info["pubType"]

        publication = get_info["prism:publicationName"]
        publication = publication.replace("'","")
        publication_type = get_info["prism:aggregationType"]

        if "prism:volume" not in get_info:
            volume = "N/A"

        else:
            volume = get_info["prism:volume"]

        if "prism:issueIdentifier" not in get_info:
            number = "N/A"

        else:
            number =  get_info["prism:issueIdentifier"]

        if "prism:startingPage" not in get_info:
            pages = "N/A"

        elif "prism:endingPage" not in get_info:
            pages = get_info["prism:startingPage"]

        else:
            pages =  get_info["prism:startingPage"] + "-" +  get_info["prism:endingPage"]

        if "dc:description" not in get_info:
            description = None

        elif get_info["dc:description"] == None:
            description = None

        else:
            description = get_info["dc:description"]
            description = description.replace("'","")

        if "originalText" not in get_data:
            full_text = None

        else:
            full_text = get_data["originalText"]
            full_text = full_text.replace("'","")


        article_data = {"AUTHORS":authors,"YEAR":year,"TITLE":title, "CATEGORY": category, "PUBLICATION":publication,"TYPE":publication_type,"VOLUME":volume,"NUMBER":number,"PAGES":pages,
        "DESCRIPTION":description,"PII":pii, "WEBURL":weburl, "FULL_TEXT":full_text}

    return article_data


def get_articles(arguments, size):
    url = "http://api.elsevier.com/content/search/index:SCIDIR?query=" + arguments + "&APIKey=" + apikey + "&httpAccept=application/json&count=" + str(size)

    pii_list = []
    req = requests.get(url)

    if req.ok == False:
        return "Error"

    else:
        data = req.json()
        get_results = data["search-results"]["entry"]
        check = data["search-results"]

        if check["opensearch:totalResults"] == None:
            return "Error"

        else:
            for item in get_results:
                pii_link = str(item["prism:url"])
                pii = pii_link[44:]
                pii_list.append(pii)


    return pii_list



#testing
#print get_article_info("DOI:10.1016/j.amjcard.2014.12.033")
#print get_article_info("DOI:10.1016/j.jhealeco.2012.04.004")
#url = "http://api.elsevier.com/content/article/pii:S1090312702700415?httpAccept=application/json&APIKey=dbaf0b9a837d9c11ab2c5f3d09973d54"

#data dump
#test = open("testing.json", "w")
#stuff = get_article_info("S0300957214001087")
#json.dump(stuff, test, sort_keys=True, indent=4, separators=(",", ": "))
#test.close()
