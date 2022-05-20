import argparse
import json
import os
import sys
from elasticsearch7 import Elasticsearch
import jieba

INDEX="ir-2022-coursework"
DOC_TYPE="document"

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    # parser.add_argument("-s","--src",help="source path", required=True)
    parser.add_argument("--rebuild-dataset", help="Clear exist data?", action="store_true")
    parser.add_argument("--debug", help="Debug?", action="store_true")
    args=parser.parse_args()

    src_path="./"
    rebuild_dataset=args.rebuild_dataset
    debug=args.debug

    es=Elasticsearch("http://localhost:9200")

    if rebuild_dataset:
        try:
            es.indices.delete(INDEX)
        except:
            pass
        es.indices.create(INDEX)
        es.indices.put_mapping(index=INDEX, include_type_name=True, doc_type=DOC_TYPE, body={
            'properties': {
                'tokenized_text': {
                    'type': 'text',
                    'analyzer': 'whitespace',
                    'search_analyzer': 'whitespace'
                },
            }
        })

    data = []
    for fn in os.listdir(src_path):
        if fn.endswith(".json"):
            with open(fn,"r",encoding = "utf-8") as f:
                curr_data = json.load(f)
                curr_data = list(curr_data.values())
                for k in range(len(curr_data)):
                    curr_data[k]["source_file"] = fn
            data.extend(curr_data)
    
    n=len(data)
    for i,doc in enumerate(data):
        if i%100==0:
            print("{} / {}".format(i,n),end='\r')
        text = list(jieba.cut(doc["title"])) + list(jieba.cut(doc["content"]))
        doc["tokenized_text"] = ' '.join(text)
        es.index(index=INDEX,doc_type=DOC_TYPE,body=doc)
