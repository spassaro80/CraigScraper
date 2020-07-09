from django.shortcuts import render
from django.views.generic.base import TemplateView
from bs4 import BeautifulSoup
import requests


def index(request):
    return render(request, 'core/index.html' )

def scraper(request):
    input1 = request.POST['input1']
    input2 = request.POST['input2']
    input3 = request.POST['input3']
# Gather user inputted search terms. In this example I want to search for (color) + (brand) + super. Color and brand
# will change as the script changes the search terms
# User inputted search terms to loop through
# Try list 1: 'red black blue white orange' and list 2: 'nike adidas reebok' and static terms: 'super+cool'
# The dynamic table would be 6x4 in this case. Always ("terms in list_1 + 1"  x  "terms in list_2 + 1")
    list_1 = input1.split(',')
    list_2 = input2.split(',')
    static_search_terms = input3

    combined_list_search_terms = [ [] for j in range(len(list_2)) ]
    for i,l1 in enumerate(list_1):
        for x,l2 in enumerate(list_2):
            combined_list_search_terms[x].append(l1 + '+' + l2)


    urls = []

    # Craigslist get number of results for each search
    result1 = [ [] for j in range(len(list_2)) ]
    for j in range(len(list_2)):
        result1[j].append(list_2[j])
    for i,rows in enumerate(combined_list_search_terms):
        for j,columns in enumerate(rows):
            url = 'https://newyork.craigslist.org/search/sss?query=' + columns + '+' + static_search_terms
            urls.append(url)
            data = requests.get(url)
            soup = BeautifulSoup(data.text, 'html.parser')
            match = soup.find('span', class_="totalcount")
            if match is not None:
                result1[i].append(int(match.text))
            else:
                result1[i].append(0)




#        a = 0
#        while a <= len(combined_list_search_terms[a])-1:
#            url = 'https://newyork.craigslist.org/search/sss?query=' + combined_list_search_terms[a] + '+' + static_search_terms
#            urls.append(url)
#            data = requests.get(url)
#            soup = BeautifulSoup(data.text, 'html.parser')
#            match = soup.find('span', class_="totalcount")
#            if match is not None:
#                r.append(match.text)
#            else:
#                r.append(0)
#            a = a + 1

    # List of hyper links of searches, and names of the search results

    i = 0
    result2 = []
    result3 = []
    result4 = [ [] for j in range(len(urls)) ]

    for i,url in enumerate(urls):
        data = requests.get(urls[i])
        soup = BeautifulSoup(data.text, 'html.parser')
        match = soup.findAll('a', class_="result-title hdrlnk")
        num = soup.find('span', class_="totalcount")
        if num is None:
            count = 0
        else:
            count = int(num.text)
        for m in match[0:int(count)]:
            if m.text is not None:
                result4[i].append(m.text)


    while i <= len(combined_list_search_terms)-1:
        result2.append(urls[i])
        data = requests.get(urls[i])
        soup = BeautifulSoup(data.text, 'html.parser')
        match = soup.findAll('a', class_="result-title hdrlnk")
        num = soup.find('span', class_="totalcount")
        if num is None:
            count = 0
        else:
            count = int(num.text)
        for j in range(count):
            if match[j].text is not None:
                result3.append(match[j].text)
        i = i + 1

    context = {'input1' : list_1, 'input2' : list_2, 'input3': input3, 'result1': result1, 'links': urls,  'result3': result3, 'result4': result4} 
    return render(request, 'core/results.html', context)

    # The output of the console is a set of 15 numbers corresponding to the 15 searches (5x3 variables in each list)
    # The output needs to be displayed back to the user as a 6x4 table (1 extra row and column for headers) on the site
    # The other output of the console is each URL searched and corresponding titles of the results searched underneath them
