import json
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
import pickle
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
import os
import pyterrier as pt


import unicodedata
import re

import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

def remove_nonalphanum(text):
  pattern = re.compile('[\W_]+')
  return pattern.sub(' ', text)

def normalize_to_english(text): 
    text = text.lower()

    # normalize to decompose characters (e.g., "â" -> "â")
    normalized_text = unicodedata.normalize('NFD', text)
    # remove diacritic marks using regex (e.g., "â" -> "a")
    normalized_text = re.sub(r'[\u0300-\u036f]', '', normalized_text)
    return normalized_text


def search(query, docno=None):
    
    if not pt.started():
        pt.init()
    

    # if request.method == 'POST':
    #     print(request.POST)
    #     query = request.POST.get("query")
    stop_words = set(stopwords.words('english'))

    stemmer = pt.index.TerrierStemmer('porter')
    query = normalize_to_english(remove_nonalphanum(query))
    cleaned = [i for i in query.split() if i not in stop_words]
    cleaned = [stemmer.stem(i) for i in cleaned]
    cleaned = " ".join(cleaned)
    cleaned = cleaned.strip()
    result = ""
    file_path = os.path.join(os.getcwd(), "model.pkl")
    with open(file_path, "rb") as f:
        model = pickle.load(f)
        queries_df = pd.DataFrame([{"qid": "1", "query": cleaned}])
        
        result = model.transform(queries_df).sort_values(by=['rank'], ascending=[ True])[:30]
        

        docnos = result['docno']  
        # print('docnos')
        # print(docnos)
        collections = pd.read_csv('search/collections.csv')
        text_and_abstract = collections[collections['docno'].isin(docnos)]
        result = pd.merge(result, text_and_abstract, on='docno', how='left')
        # print(result)
        result_json = result.to_dict(orient="records")

        return result_json
    return None




@csrf_exempt
def home(request):
    stop_words = set(stopwords.words('english'))
    results = []
    query = ""

    if not pt.started():
        pt.init()
    
    if request.method == "POST":
        # print(request.POST)
        query = request.POST.get("query")
        results = search(query)
        request.session['results'] = results 
        # print("ini result")
        # print((results))
        if not results:
            return HttpResponseNotFound("No Documents Found for the Query")
            # results = result['message']
            
            # print(results)
            # results = [{"rank": 1, "docno": 12, "docname": "hello", "score": 123}, {"rank": 2, "docno": 13, "docname": "world", "score": 100}, {"rank": 1, "docno": 12, "docname": "hello", "score": 123}, {"rank": 2, "docno": 13, "docname": "world", "score": 100}]
        # else: 
            # return HttpResponseNotFound("No Documents Found for the Query")
    
    return render(request, "serp.html", {"query": query, "results": results})

def detail(request, docno):
    results = request.session.get('results', None)
    # print(results)
    if results is None:
        return render(request, 'detail.html', {'message': 'No document data found.'})

    document = pd.DataFrame(results)
    # print(document)
    data = document[document['docno'] == docno]
    data_json = data.to_dict(orient="records")[0]
    print("ini data")
    print(data_json)
    # print(result)
    # document = {"rank": 1, "docno": docno, "docname": "hello", "score": 123}
    return render(request, 'detail.html', {'document': data_json})

def hi(request):
    return  JsonResponse({
            "status": True,
            "message": "hi",
            }, status=200)