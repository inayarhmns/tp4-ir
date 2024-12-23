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
            result = model.transform(queries_df).sort_values(by=['rank'], ascending=[ True])[:30]
           
            result_json = result.to_dict(orient="records")

        


        return JsonResponse({
            "status": True,
            "message": result_json,
            }, status=200)
    return HttpResponseNotFound()


def hi(request):
    return  JsonResponse({
            "status": True,
            "message": "hi",
            }, status=200)