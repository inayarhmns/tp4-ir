from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
import pickle
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
import os
import pyterrier as pt


import unicodedata
import re

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

@csrf_exempt
def search(request):
    
    if not pt.started():
        pt.init()
    

    if request.method == 'POST':
        print(request.POST)
        query = request.POST.get("query")
        query = normalize_to_english(remove_nonalphanum(query))
        print(query)
        result = ""
        file_path = os.path.join(os.getcwd(), "model.pkl")
        with open(file_path, "rb") as f:
            model = pickle.load(f)
            queries_df = pd.DataFrame([{"qid": "1", "query": query}])
            result = model.transform(queries_df).sort_values(by=['rank'], ascending=[ True])[:50]
           
            result_json = result.to_dict(orient="records")

        


        return JsonResponse({
            "status": True,
            "message": result_json,
            }, status=200)
    return HttpResponseNotFound()

def home(request):
    results = []
    query = ""

    if not pt.started():
        pt.init()
    
    if request.method == "POST":
        query = request.POST.get("query", "")
        query = normalize_to_english(remove_nonalphanum(query))

        # dummy
        results = [{"rank": 1, "docno": 12, "docname": "hello", "score": 123}, {"rank": 2, "docno": 13, "docname": "world", "score": 100}, {"rank": 1, "docno": 12, "docname": "hello", "score": 123}, {"rank": 2, "docno": 13, "docname": "world", "score": 100}]

        # Load the model
        # file_path = os.path.join(os.getcwd(), "model.pkl")
        # with open(file_path, "rb") as f:
        #     model = pickle.load(f)
        #     queries_df = pd.DataFrame([{"qid": "1", "query": query}])
        #     result = model.transform(queries_df).sort_values(by=['rank'], ascending=True)[:50]
        #     results = result.to_dict(orient="records")
    
    return render(request, "serp.html", {"query": query, "results": results})

def detail(request, docno):
    document = {"rank": 1, "docno": docno, "docname": "hello", "score": 123}
    return render(request, 'detail.html', {'document': document})

def hi(request):
    return  JsonResponse({
            "status": True,
            "message": "hi",
            }, status=200)