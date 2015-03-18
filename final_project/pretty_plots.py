#Loading and Decoding#
from io import open
import json
import pymysql
#from os import remove
#from os.path import exists
import matplotlib
import matplotlib.pyplot as plt
import numpy as np





##################################


dbname="Final_Project"
host="localhost"
user="root"
passwd="Fanficfan2"
db=pymysql.connect(db=dbname, host="127.0.0.1", user=user,passwd=passwd, charset="utf8")
c = db.cursor()


##################################


def author_table(): #Table


    get_main_authors = """SELECT Authors from authors"""
    get_reference_authors = """SELECT Authors from reference_authors"""
    get_recommendation_authors = """SELECT Authors from recommended_authors"""

    author_dict = {}
    main_authors = []
    reference_authors = []
    recommendation_authors = []
    author_list =  []
    c.execute(get_main_authors)
    for author in c:
        curated = str(author)[3:-3]
        main_authors.append(curated)
    c.execute(get_reference_authors)
    for author in c:
        curated = str(author)[3:-3]
        reference_authors.append(curated)
    c.execute(get_recommendation_authors)
    for author in c:
        curated = str(author)[3:-3]
        recommendation_authors.append(curated)

    author_list =  main_authors + reference_authors + reference_authors

    while '' in author_list:
        author_list.remove('')

    for author in author_list:
        if author in author_dict:
            author_dict[author] += 1
        else:
            author_dict[author] = 1


    return author_dict


def journal_table(): #HBar Chart

    get_main_journals = """SELECT Publication from article_data"""
    get_reference_journal = """SELECT Publication from reference_data"""
    get_recommendation_journal = """SELECT Publication from recommended_articles"""

    journals_dict = {}
    main_journals = []
    reference_journals = []
    recommendation_journals = []
    journal_list = []
    c.execute(get_main_journals)
    for journal in c:
        curated = str(journal)[3:-3]
        main_journals.append(curated)
    c.execute(get_reference_journal)
    for journal in c:
        curated = str(journal)[3:-3]
        reference_journals.append(curated)
    c.execute(get_recommendation_journal)
    for journal in c:
        curated = str(journal)[3:-3]
        recommendation_journals.append(curated)


    journal_list = main_journals + reference_journals + recommendation_journals

    while '' in journal_list:
        journal_list.remove('')
    while 'N/A' in journal_list:
        journal_list.remove('N/A')

    for journal in journal_list:
        if journal in journals_dict:
            journals_dict[journal] += 1
        else:
            journals_dict[journal] = 1

    jxvals = sorted(journals_dict.keys())
    jyvals = []
    for x in jxvals:
        jyvals.append(journals_dict[x])
    plt.barh(range(len(journals_dict)), jyvals, align='center', color='#CC0000')
    plt.yticks(range(len(journals_dict)), jxvals)
    plt.xlabel('Frequency')
    plt.ylabel('Journals')
    plt.title('Frequency of Appearance for Journals')
    plt.savefig('static/journals.png', bbox_inches='tight')
    plt.clf()
    plt.close()


def availability(): #Pie Chart

    get_references_count = """SELECT Status from reference_data"""

    c.execute(get_references_count)
    ref_list = []
    for status in c:
        curate = str(status)[3:-3]
        ref_list.append(curate)

    available = 0
    partly = 0
    unavailable = 0
    status_count = {'Available':0, 'Partly Available':0, 'Unavailable':0}

    for status in ref_list:
        if status == 'Available via Elsevier':
            status_count['Available'] += 1
        elif status == 'Available via external Link':
            status_count['Partly Available'] += 1
        elif status == 'Unavailable':
            status_count['Unavailable'] += 1

    available = status_count['Available']
    partly = status_count['Partly Available']
    unavailable = status_count['Unavailable']
    labels = 'Fully Available', 'Available via External Link', 'Unavailable'
    sizes = [available, partly, unavailable]
    colors = ['yellowgreen', 'lightskyblue', 'lightcoral']
    explode = (0.1, 0, 0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')
    plt.title('General Availability of Collected References')
    plt.savefig('static/availability.png', bbox_inches='tight')
    plt.clf()
    plt.close()


def year_chart(): #Bar Chart

    get_main_years = """SELECT Pub_Year from article_data"""
    get_reference_years = """SELECT Pub_Year from reference_data WHERE Status='available via elsevier'"""
    get_recommendation_years = """SELECT Pub_Year from recommended_articles"""

    all_years =  []
    years_list = []
    years_dict = {}
    main_years = []
    reference_years = []
    recommendation_years = []
    xvals = 0

    c.execute(get_main_years)
    for year in c:
        curated = str(year)[3:-3]
        main_years.append(curated)
    c.execute(get_reference_years)
    for year in c:
        curated = str(year)[3:-3]
        reference_years.append(curated)
    c.execute(get_recommendation_years)
    for year in c:
        curated = str(year)[3:-3]
        recommendation_years.append(curated)

    all_years =  main_years + reference_years + recommendation_years

    years_list = ['N/A' if year == '' else year for year in all_years]

    for year in years_list:
        if year in years_dict:
            years_dict[year] += 1
        else:
            years_dict[year] = 1

    yxvals = sorted(years_dict.keys(), key=int)
    yyvals = []
    for x in yxvals:
        yyvals.append(years_dict[x])
    plt.bar(range(len(years_dict)), yyvals, align='center', color='m')
    plt.xticks(range(len(years_dict)), yxvals)
    plt.xlabel('Year of Publication')
    plt.ylabel('Frequency')
    plt.title('Years of Publication for All Available Articles')
    plt.savefig('static/year_chart.png', bbox_inches='tight')
    plt.clf()
    plt.close()


def category_chart(): #HBar Chart

    get_article_categories = """SELECT Category from article_data"""
    get_reference_categories = """SELECT Category from reference_data WHERE Status='Available via Elsevier'"""
    get_recommendation_categories = """SELECT Category from recommended_articles"""

    categories_dict = {}
    main_categories = []
    reference_categories = []
    recommendation_categories = []
    xvals = 0
    categories_list = []
    c.execute(get_article_categories)
    for category in c:
        curated = str(category)[3:-3]
        main_categories.append(curated)
    c.execute(get_reference_categories)
    for category in c:
        curated = str(category)[3:-3]
        reference_categories.append(curated)
    c.execute(get_recommendation_categories)
    for category in c:
        curated = str(category)[3:-3]
        recommendation_categories.append(curated)

    categories_list = main_categories + reference_categories + recommendation_categories

    for category in categories_list:
        if category in categories_dict:
            categories_dict[category] += 1
        else:
            categories_dict[category] = 1

    cxvals = sorted(categories_dict.keys())
    cyvals = []
    for x in cxvals:
        cyvals.append(categories_dict[x])
    plt.barh(range(len(categories_dict)), cyvals, align='center')
    plt.yticks(range(len(categories_dict)), cxvals)
    plt.xlabel('Frequency')
    plt.ylabel('Categories')
    plt.title('Article Categories for All Directly Available Articles')
    #plt.show()
    plt.savefig('static/categories.png', bbox_inches='tight')
    plt.clf()
    plt.close()


def available_counts(): #Stacked Histogram

    get_main_counts = """SELECT Citation_Count from article_data"""
    get_reference_counts = """SELECT Citation_Count from reference_data WHERE Status='Available via Elsevier'"""
    get_recommendation_counts = """SELECT Citation_Count from recommended_articles"""

    counts_dict = {}
    main_counts = []
    reference_counts = []
    recommendation_counts = []
    all_counts =  []
    c.execute(get_main_counts)
    for count in c:
        curated = str(count)[3:-3]
        main_counts.append(curated)
    c.execute(get_reference_counts)
    for count in c:
        curated = str(count)[3:-3]
        reference_counts.append(curated)
    c.execute(get_recommendation_counts)
    for count in c:
        curated = str(count)[3:-3]
        recommendation_counts.append(curated)

    all_counts =  main_counts + reference_counts + recommendation_counts

    while '' in all_counts:
        all_counts.remove('')
    while 'N/A' in all_counts:
        all_counts.remove('N/A')

    xvals = []
    for count in all_counts:
        xvals.append(int(count))

    return xvals


def partly_available_counts(): #Stacked Histogram

    get_reference_counts = """SELECT Citation_Count from reference_data WHERE Status='Available via external Link'"""

    counts_dict = {}
    reference_counts = []

    c.execute(get_reference_counts)
    for count in c:
        curated = str(count)[3:-3]
        reference_counts.append(curated)

    while '' in reference_counts:
        reference_counts.remove('')
    while 'N/A' in reference_counts:
        reference_counts.remove('N/A')

    count_list = []
    for count in reference_counts:
        count_list.append(int(count))

    return count_list

def unavailable_counts(): #Stacked Histogram

    get_reference_counts = """SELECT Citation_Count from reference_data WHERE Status='Unavailable'"""

    counts_dict = {}

    reference_counts = []

    c.execute(get_reference_counts)
    for count in c:
        curated = str(count)[3:-3]
        reference_counts.append(curated)

    while '' in reference_counts:
        reference_counts.remove('')
    while 'N/A' in reference_counts:
        reference_counts.remove('N/A')


    count_list = []
    for count in reference_counts:
        count_list.append(int(count))

    return count_list



def counts_histogram():

    available = available_counts()
    partly_available = partly_available_counts()
    unavailable = unavailable_counts()
    alabels = ['Available', 'Partly Available', 'Unavailable']
    plt.hist([available, partly_available, unavailable], label=alabels, bins=5)
    plt.xlabel('Number of Times Cited')
    plt.ylabel('Frequency')
    plt.title('Citation Counts for All Articles by Availability')
    plt.legend()
    #plt.show()
    plt.savefig('static/citation_counts.png', bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()
