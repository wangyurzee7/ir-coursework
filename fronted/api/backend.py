from elasticsearch7 import Elasticsearch
import jieba

INDEX="ir-2022-coursework"
DOC_TYPE="document"

def init():
    global es
    es=Elasticsearch(host='localhost', port=9200)

def search(text, start, count):
    if type(text) == str:
        text = list(jieba.cut(text))
    if type(text) == list:
        text = ' '.join(text)
    global es
    ret = es.search(
        index=INDEX,
        doc_type=DOC_TYPE,
        body={
            "from": start,
            "size": count,
            "query": {
                "query_string": {
                    "query": text
                }
            }
        }
    )
    ret["query"] = text
    ret["start"] = start
    ret["count"] = count
    return ret

'''
def detail(index):
    global es
    return es.get(
        index=INDEX,
        doc_type=DOC_TYPE,
        id=index
    )["_source"]
'''