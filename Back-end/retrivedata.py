from flask import Flask, render_template
from elasticsearch import Elasticsearch

app = Flask(__name__)
ELASTIC_PASSWORD = "td-302HyXw2HxZrJHBib"
es = Elasticsearch("https://localhost:9200", http_auth=("elastic", ELASTIC_PASSWORD), verify_certs=False)

@app.route('/song/<song_id>')
def song_page(song_id):
    index_name = 'song_data'
    response = es.get(index_name, id=song_id)
    song_data = response["_source"]
    return render_template("Front-End/Result.html", song=song_data)

if __name__ == '__main__':
    app.run(debug=True)