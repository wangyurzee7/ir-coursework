from elasticsearch import Elasticsearch
import json
import numpy as np

INDEX="ir-coursework"
DOC_TYPE="document"

word2vec=json.load(open("../dataset/wiki_word2vec.json","r"))
UNK=[1e-7 for i in range(300)]

def init():
    global es
    es=Elasticsearch(host='localhost', port=9200)

def search(text,page=1):
    global es
    if text.startswith("word2vec:"):
        text_arr=text.replace("word2vec:","").split(' ')
        vector_arr=[]
        for word in text_arr:
            word=word.split("_")[0]
            if word in word2vec:
                vector_arr.append(word2vec[word])
            else:
                vector_arr.append(UNK)
        vector_arr=np.array(vector_arr).T
        max_pooling=np.max(vector_arr,axis=1).tolist()
        avg_pooling=np.mean(vector_arr,axis=1).tolist()
        min_pooling=np.min(vector_arr,axis=1).tolist()
        input_vector=max_pooling+avg_pooling+min_pooling
        return es.search(
            index=INDEX,
            doc_type=DOC_TYPE,
            body={
                "from": 20*(page-1),
                "size": 20,
                "query": {
                    "script_score": {
                        "query": {
                            "match_all": {}
                        },
                        "script": {
                            "source": "cosineSimilarity(params.queryVector, 'vector')+1",
                            "params": {
                                "queryVector": input_vector
                            }
                        }
                    }
                }
            }
        )
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
