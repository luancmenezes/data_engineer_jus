from flask import Flask, render_template, request, json
import json
from elasticsearch import Elasticsearch
import os
app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
value = ''
def json2html(res):
    for doc in res['hits']['hits']:
        yield doc['_source']
def scrapy_2_elasticSearch(nprocesso):
#     os.chdir('crawlers_tribunais/')
    os.system('cd crawlers_tribunais/ && scrapy crawl tribunal -a processo={}'.format(nprocesso))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/searchengine', methods=['POST', 'GET']) 
def search():
    index = "tbj"
    response = ''
    nprocesso = request.form.get('nprocesso')

    if es.indices.exists(index=index):
        res = es.search(index=index,  body={"query": 
                                           {"multi_match":
                                           {"query":nprocesso,
                                           "fields": [ "processo", "processo_2" ]}}})
        if res['hits']['max_score']:
            response = json2html(res)
        else:
           scrapy_2_elasticSearch(nprocesso) 
    else:
        scrapy_2_elasticSearch(nprocesso) 
        res = es.search(index=index,  body={"query": 
                                           {"multi_match":
                                           {"query":nprocesso,
                                           "fields": [ "processo", "processo_2" ]}}})
        if res['hits']['max_score']:
            response = json2html(res)
        

    return render_template('index.html',documents=list(response))

if __name__ == '__main__':
    app.run(host='localhost', port=9874)