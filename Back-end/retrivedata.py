from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from markupsafe import escape
import math

app = Flask(__name__, template_folder="../Front-end", static_folder="../Front-end/css")
ELASTIC_PASSWORD = "td-302HyXw2HxZrJHBib"
es = Elasticsearch("https://localhost:9200", http_auth=("elastic", ELASTIC_PASSWORD), verify_certs=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    page_size = 10
    keyword = request.args.get('keyword')
    if request.args.get('page'):
        page_no = int(request.args.get('page'))
    else:
        page_no = 1
        
    body = {
        'size' : page_size,
        'from' : page_size * (page_no-1),
        'query' : {
            'multi_match': {
                'query' : keyword,
                'fields' : ['Name', 'Description', 'Genre', 'Artist', 'Lyrics', 'Producer', 'Songwriter', 'Release Date']
            }
        }
    }
    
    res = es.search(index='song_data', body=body)
    hits = [{'Name': doc['__source']['Name'], 'Description': doc['__source']['Description'], 
             'Genre': doc['__source']['Genre'], 'Artist': doc['__source']['Artist'],
             'Lyrics': doc['__source']['Lyrics'], 'Producer': doc['__source']['Producer'],
             'Songwriter': doc['__source']['Songwriter'], 'Release Date': doc['__source']['Release Date']} for doc in res['hits']['hits']]
    page_total = math.ceil(res['hits']['total']['value']/page_size)
    return render_template('search.html', keyword=keyword, hits=hits, page_no=page_no, page_total=page_total)

@app.route('/song/<song_id>')
def song_page(song_id):
    response = es.get(index='song_data', id=song_id)
    song_data = response["_source"]
    return render_template("Result.html", 
                           Name=song_data.get("Name", ""),
                           Artist=song_data.get("Artist", ""),
                           Genre=song_data.get("Genre", ""),
                           Release_Date=song_data.get("Release Date", ""),
                           Producer=song_data.get("Producer", ""),
                           Songwriter=song_data.get("Songwriter", ""),
                           Description=song_data.get("Description", ""),
                           Lyrics=song_data.get("Lyrics", ""),
                           Position=song_data.get("Position in chart", ""),
                           Stream=song_data.get("Streams", ""))

if __name__ == '__main__':
    app.run(debug=True)