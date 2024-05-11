from flask import Flask, render_template, send_file, request
import pymongo
from gridfs import GridFS
from bson.objectid import ObjectId
import json


# Initialize Flask app
app = Flask(__name__)


client = pymongo.MongoClient("mongodb://10.49.15.188:27017/")
db = client["TA5K_SDX631QV"]
# collection = db["build-ML-300"]
fs = GridFS(db)



@app.route('/')
def home():
    # db = client["TA5K_SDX631QV"]
    # try:
    collections=[name for name in db.list_collection_names() if name.startswith('branch') ]
    collection_data={}

    for collection_name in collections:
        collection_data[collection_name]=list(db[collection_name].find())
    # except Exception as e:
    #     return {'error':str(e)}
    # collection = db["branch-ML-300"]
    # documents = list(collection.find({}))
    return render_template('home.html', collections=collection_data)


@app.route('/index/<collection_name>/<document_id>')
def index(collection_name, document_id):
    document = db[collection_name].find_one({'_id': ObjectId(document_id)})
    build_name=document.get('build')
    
    documents = list(collection.find({}))
    return render_template('index.html', documents=documents)

  

@app.route('/view-html')
def view_html():
    db = client["TA5K_SDX631QV"]
    fs = GridFS(db, collection='ML-300')
    filename = request.args.get('filename')
    file = fs.find_one({'filename': filename})
    if file:
        html_content = file.read().decode('utf-8')
        return html_content
    else:
        return "File not found"


if __name__ == "__main__":
    app.run(debug=True)
