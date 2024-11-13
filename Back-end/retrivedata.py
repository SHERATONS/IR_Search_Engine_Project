from flask import Flask, render_template
from elasticsearch import Elasticsearch

app = Flask(__name__, template_folder="../Front-end", static_folder="../Front-end/css")
ELASTIC_PASSWORD = "td-302HyXw2HxZrJHBib"
es = Elasticsearch("https://localhost:9200", http_auth=("elastic", ELASTIC_PASSWORD), verify_certs=False)

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