import json
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    #return "Hello world !"
    return render_template_string("<h1>"Hello world !"<h1> <br>")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)