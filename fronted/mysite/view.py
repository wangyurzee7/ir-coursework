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

srcPath='../news/'

def index(request):
	return render(request,"index.html")


countPerPage=20
dateFormat='%Y-%m-%d'
def search(request):
	try:
		keyword=request.GET['keyword']
	except:
		return index(request)
	try:
		page=int(request.GET['page'])
	except:
		page=1
	
	obj={"news":[]}
	startTime=time.time()
	result=api.search(keyword,page=page)
	doc_list=result["hits"]["hits"]
	obj["searchTime"]='{0:.5f}'.format(time.time()-startTime)

	keyWords=[]
	for word in keyword.split(' '):
		keyWords.append(word.split('_')[0])
	for doc in doc_list:
		news=doc["_source"]
		news["index"]=doc["_id"]
		news["content"]=news["text"].replace(' ','')
		if len(news["content"])>30:
			news["title"]=news["content"][:29]+"…"
		else:
			news["title"]=news["content"]
		for k in keyWords:
			news["title"]=news["title"].replace(k,'<em>'+k+'</em>')
		news["brief"]=news["content"]
		for k in keyWords:
			if news["brief"].count(k)>0:
				news["brief"]=news["brief"].replace(k,'<em>'+k+'</em>')
		obj["news"].append(news)
	obj["pages"]=[]
	newsSum=result["hits"]["total"]["value"]
	ellipsis="<a>...</a>"
	for i in range(1,(newsSum-1)//countPerPage+2):
		if i==1 or i==(newsSum-1)//countPerPage+1 or abs(i-page)<5:
			if (i!=page):
				#<i class="c-icon c-icon-bear-pn"></i><span class="fk"></span><span class="pc"> removed
				newObj='<a href="/search/?keyword={0}&go=Search&page={1}">{2}</a>'.format(keyword,i,i)
			else:
				newObj='<strong>{0}</strong>'.format(i)
			obj["pages"].append(newObj)
		else:
			if obj["pages"][-1]!=ellipsis:
				obj["pages"].append(ellipsis)
	obj["newsCount"]=newsSum
	obj["keyword"]=keyword
	return render(request,"search.html",obj)

def detail(request,num):
	# HttpResponse(os.system("ls "+srcPath))
	index=num
	news=api.detail(index)
	if not news:
		raise Http404
	news["content"]=news["text"].replace(' ','')
	news["title"]=news["content"][:50]
	return render(request,"detail.html",news)
