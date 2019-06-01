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
# def scrapyCall():

@app.route('/')
def home():
    print(es)
    return render_template('index.html')

@app.route('/searchengine', methods=['POST', 'GET']) 
def search():
    index = "tbj"
    nprocesso = request.form.get('nprocesso')

    if es.indices.exists(index=index):
        res = es.search(index=index,  body={"query": {"match": {'processo':nprocesso}}})
        if res['hits']['max_score']:
            response = json2html(res)
        else:
            os.chdir('crawlers_tribunais/')
            os.system('scrapy crawl tribunal -a processo={}'.format(nprocesso))
    else:
        os.chdir('crawlers_tribunais/')
        os.system('scrapy crawl tribunal -a processo="{}"'.format(nprocesso))
        res = es.search(index=index,  body={"query": {"match": {'processo':nprocesso}}})
        if res['hits']['max_score']:
            response = json2html(res)
        else:
            response = None

    return render_template('index.html',documents=list(response))

if __name__ == '__main__':
    app.run(host='localhost', port=9874)