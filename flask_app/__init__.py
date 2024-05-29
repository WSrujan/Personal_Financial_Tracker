from flask import Flask
app = Flask(__name__)

app.secret_key = "shhhhhhhhhhh"
DB_NAME = "finance_tracker_schema"