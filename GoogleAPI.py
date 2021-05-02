from flask import Flask
from flask import render_template

app= Flask(__name__)

@app.route('/')
def index():
  return render_template('google175fe4a0c26aaf2b.html')