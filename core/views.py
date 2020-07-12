from django.shortcuts import render
from django.views.generic.base import TemplateView
from bs4 import BeautifulSoup
import requests

def index(request):
    return render(request, 'core/index.html' )

def bones_scraper(request):

    input1 = request.POST['input1']
    input2 = request.POST['input2']
    input3 = request.POST['input3']

    list_1 = input1.split(',')
    list_2 = input2.split(',')
    static_search_terms = input3

    combined_list_search_terms = [ [] for j in range(len(list_2)) ]
    for i,l1 in enumerate(list_1):
        for x,l2 in enumerate(list_2):
            combined_list_search_terms[x].append(l1 + '+' + l2)


    urls = []

    # Pubmed get number of results for each search

    #Create an empty table of 2 dimensions. N of columns will be = nº search terms of input2

    result_table = [ [] for j in range(len(list_2)) ]
    
    #For every row, the first element will be the name of search term of input 1
    
    for j in range(len(list_2)):
        result_table[j].append(list_2[j])

    #Loop for every element of the table and populate with the nº of result

    for i,rows in enumerate(combined_list_search_terms):
        for j,columns in enumerate(rows):
            url = 'https://pubmed.ncbi.nlm.nih.gov/?term=' + columns + '+' + static_search_terms + '+%28autograft+OR+autogenous+OR+autologous%29&filter=species.humans&filter=language.english&size=200'
            urls.append(url)
            data = requests.get(url)
            soup = BeautifulSoup(data.text, 'lxml')
            match = soup.find('span', class_="value")
            if match is not None:
                result_table[i].append(int(match.text))
            else:
                result_table[i].append(0)


    #url_results will be a dictionary where the keys are the urls scraped and the values will be arrays. Each array has the results of the urls scraped.
    # For example: if we have url1 and url2, with 2 and 1 result scraped, the dictionary will be:
    # url_results = {'url1' :[result1_url1, result1_url1], 'url2' : [result1_url2] }
    url_results = {}

    for i,url in enumerate(urls):
        data = requests.get(urls[i])
        url_results[urls[i]] = []
        soup = BeautifulSoup(data.text, 'lxml')
        match = soup.findAll('a', class_="labs-docsum-title")
        num = soup.find('span', class_="value")
        if num is None:
            count = 0
        else:
            count = int(num.text)
        for m in match[0:int(count)]:
            if m.text is not None:
                url_results[urls[i]].append(m.text.strip())


    context = {'input1' : list_1, 'result_table': result_table, 'links': urls, 'url_results': url_results} 
    return render(request, 'core/results.html', context)

    # The output of the console is a set of 15 numbers corresponding to the 15 searches (5x3 variables in each list)
    # The output needs to be displayed back to the user as a 6x4 table (1 extra row and column for headers) on the site
    # The other output of the console is each URL searched and corresponding titles of the results searched underneath them

 