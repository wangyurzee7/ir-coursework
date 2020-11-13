from elasticsearch import Elasticsearch

INDEX="ir-coursework"
DOC_TYPE="document"

def init():
    global es
    es=Elasticsearch(host='localhost', port=9200)

def search(text,page=1):
    global es
    return es.search(
        index=INDEX,
        doc_type=DOC_TYPE,
        body={
            "from": 20*(page-1),
            "size": 20,
            "query": {
                "query_string": {
                    "query": text
                }
            }
        }
    )

def detail(index):
    global es
    return es.get(
        index=INDEX,
        doc_type=DOC_TYPE,
        id=index
    )["_source"]
