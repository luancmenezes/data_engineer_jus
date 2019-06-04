import os
from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)

es = Elasticsearch([{'host': 'localhost', 'port': 9200}], http_auth=('elastic', 'root'))


def json2html(res):
    for doc in res['hits']['hits']:
        yield doc['_source']
def scrapy_2_elasticSearch(nprocesso):
#     os.chdir('crawlers_tribunais/')
    os.system('cd crawlers_tribunais/ && scrapy crawl tribunal -a processo={}'.format(nprocesso))

@app.route('/')
def home():
    print(es)
    return render_template('index.html')


@app.route('/searchengine', methods=['POST','GET'])
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
    print("AQUI_2 {}".format(nprocesso))

    return render_template('index.html', documents=list(response))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
