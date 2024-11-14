from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from markupsafe import escape, Markup
import math

app = Flask(__name__, template_folder="../Front-end", static_folder="../Front-end/css")
ELASTIC_PASSWORD = "td-302HyXw2HxZrJHBib"
es = Elasticsearch("https://localhost:9200", http_auth=("elastic", ELASTIC_PASSWORD), verify_certs=False)

@app.route('/')
def index():
    return render_template('search.html')

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
    hits = [{'Name': doc['_source']['Name'], 'Description': doc['_source']['Description'], 
             'Genre': doc['_source']['Genre'], 'Artist': doc['_source']['Artist'],
             'Lyrics': doc['_source']['Lyrics'], 'Producer': doc['_source']['Producer'],
             'Songwriter': doc['_source']['Songwriter'], 'Release Date': doc['_source']['Release Date'],
             'Song Image Link': doc['_source']['Song Image Link']} for doc in res['hits']['hits']]
    page_total = math.ceil(res['hits']['total']['value']/page_size)
    total_song = res['hits']['total']['value']
    return render_template('index.html', keyword=keyword, hits=hits, page_no=page_no, page_total=page_total, page_size=page_size, total_song=total_song)

@app.route('/song/<song_name>')
def song_page(song_name):
    body = {
        'query' : {
            'match' : {
                'Name' : song_name
            }
        }
    }
    response = es.search(index='song_data', body=body)
    song_data = response['hits']['hits'][0]["_source"]
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
                           Stream=song_data.get("Streams", ""),
                           Link=song_data.get("Song Image Link", ""))

@app.template_filter('newline')
def newline(value):
    return Markup(value.replace("\n", "<br>"))

if __name__ == '__main__':
    app.run(debug=True)