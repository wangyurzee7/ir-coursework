import argparse
import json
import os
import sys
from elasticsearch import Elasticsearch

INDEX="ir-coursework"
DOC_TYPE="document"

def parse_doc(line):
    arr=line.split(' ')
    text,text_pos=[],[]
    for word_pos in arr:
        try:
            word,pos=word_pos.split("_")
        except:
            continue
        text.append(word)
        text_pos.append("{}({})".format(word,pos))
    return text,text_pos

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-i","--input",help="input file", required=True)
    parser.add_argument("--rebuild-dataset", help="Clear exist data?", action="store_true")
    parser.add_argument("--debug", help="Debug?", action="store_true")
    args=parser.parse_args()

    input_file_name=args.input
    rebuild_dataset=args.rebuild_dataset
    debug=args.debug

    es=Elasticsearch(host="localhost", port=9200)

    if rebuild_dataset:
        try:
            es.indices.delete(index=INDEX,ignore=[400,404])
        except:
            pass
        es.indices.create(index=INDEX,ignore=400)
        es.indices.put_mapping(index=INDEX, include_type_name=True, doc_type=DOC_TYPE, body={
            'properties': {
                'text': {
                    'type': 'text',
                    'analyzer': 'whitespace',
                    'search_analyzer': 'whitespace'
                },
                'text_pos': {
                    'type': 'text',
                    'analyzer': 'whitespace',
                    'search_analyzer': 'whitespace'
                },
            }
        })

    
    with open(input_file_name,"r") as f:
        data=f.read().split('\n')
    
    n=len(data)
    for i,line in enumerate(data):
        if i%100==0:
            print("{} / {}".format(i,n),end='\r')
        if not line:
            continue
        try:
            text,text_pos=parse_doc(line)
            if not text:
                continue
            es.index(index=INDEX,doc_type=DOC_TYPE,body={
                "text": ' '.join(text),
                "text_pos": ' '.join(text_pos),
            })
        except:
            if debug:
                print(line)
                input()
            pass
