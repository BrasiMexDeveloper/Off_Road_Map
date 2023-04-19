from flask import Flask
app = Flask(__name__)
app.secret_key = "keep it secret"
DATABASE = "Off_Road_Map"