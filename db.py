from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Float


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:root@localhost/karaokedb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

