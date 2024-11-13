from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from markupsafe import escape
import math

app = Flask(__name__)
ELASTIC_PASSWORD = "td-302HyXw2HxZrJHBib"
es = Elasticsearch("https://localhost:9200", http_auth=("elastic", ELASTIC_PASSWORD), verify_certs=False)

@app.route('/')
def index():
    return render_template('index.html')