from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from YoutubePodcasts import config
import os

app = Flask(__name__) 

app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_ADDRESS
db = SQLAlchemy(app)

from YoutubePodcasts import models

if not os.path.exists(config.DATABASE_PATH):
    db.create_all()

from YoutubePodcasts import views
