from django.http import HttpResponse,Http404
from django.shortcuts import render
import os
import json
import random

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
    query=request.GET['keyword'] if 'keyword' in request.GET else ""
    start=int(request.GET['start']) if 'start' in request.GET else 0
    count=int(request.GET['count']) if 'count' in request.GET else 20
    
    result=api.search(query, start = start, count = count)
    # doc_list=result["hits"]["hits"]
    ret = {
        "total": result["hits"]["total"]["value"],
        "start": result["start"],
        "count": result["count"],
        "score": list(map(lambda x:x["_score"], result["hits"]["hits"])),
        "data": list(map(lambda x:x["_source"], result["hits"]["hits"])),
    }

    resp = HttpResponse(json.dumps(ret,ensure_ascii=False,indent=2))
    resp.__setitem__("Access-Control-Allow-Origin","*")
    return resp

data_path = "../data/"
def _get_data(src, date):
    fn = os.path.join(data_path, "{}_{}.json".format(src, date))
    if not os.path.exists(fn):
        return []
    data = json.load(open(fn, "r", encoding="utf-8"))
    data = list(data.values())
    return data

def get_random(request):
    date = request.GET['date']
    data = _get_data("weibo", date) + _get_data("zhihu", date)
    random.shuffle(data)
    ret = data[:20]
    resp = HttpResponse(json.dumps(ret,ensure_ascii=False,indent=2))
    resp.__setitem__("Access-Control-Allow-Origin","*")
    return resp

def get_weibo(request):
    date = request.GET['date']
    data = _get_data("weibo", date)
    ret = data
    resp = HttpResponse(json.dumps(ret,ensure_ascii=False,indent=2))
    resp.__setitem__("Access-Control-Allow-Origin","*")
    return resp

def get_zhihu(request):
    date = request.GET['date']
    data = _get_data("zhihu", date)
    ret = data
    resp = HttpResponse(json.dumps(ret,ensure_ascii=False,indent=2))
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