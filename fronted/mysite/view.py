from django.http import HttpResponse,Http404
from django.shortcuts import render
import os
import json

from django.conf import settings
import jieba
import re
import time
#import datetime

import api.api as api

'''
def index(request):
    return render(request,"index.html")
'''

countPerPage=20
dateFormat='%Y-%m-%d'
def search(request):
    query=request.GET['query'] if 'query' in request.GET else ""
    start=int(request.GET['start']) if 'start' in request.GET else 0
    count=int(request.GET['count']) if 'count' in request.GET else 10
    
    result=api.search(query, start = start, count = count)
    # doc_list=result["hits"]["hits"]

    resp = HttpResponse(json.dumps(result,ensure_ascii=False,indent=2))
    resp.__setitem__("Access-Control-Allow-Origin","*")
    return resp

'''
srcPath='../news/'

def detail(request,num):
    # HttpResponse(os.system("ls "+srcPath))
    index=num
    news=api.detail(index)
    if not news:
        raise Http404
    news["content"]=news["text"].replace(' ','')
    news["title"]=news["content"][:50]
    return render(request,"detail.html",news)
'''