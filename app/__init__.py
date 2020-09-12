from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mydatabase.db')
db = SQLAlchemy(app)

app.config.from_object(__name__)
from app import views
