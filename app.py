from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI= os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.han.find({},{'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    tanggal_sekarang = datetime.now()
    mytime = tanggal_sekarang.strftime('%d-%m-%Y-%H-%M-%S')
    
    file = request.files["file_give"]
    ekstensi = file.filename.split('.')[-1]
    save_file = f'static/post-{mytime}.{ekstensi}'
    file.save(save_file)

    profile = request.files["profile_give"]
    ekstensi = profile.filename.split('.')[-1]
    save_profile = f'static/profile-{mytime}.{ekstensi}'
    profile.save(save_profile)


    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')

    
    doc = {
        'nfile' : save_file,
        'nprofile' : save_profile,
        'title' : title_receive,
        'content' : content_receive,
        'date' : tanggal_sekarang 
    }
    
    db.han.insert_one(doc)
    
    return jsonify({'msg':'Upload complete!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)