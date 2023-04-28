import flask
from flask import Flask, render_template, request, Response, jsonify
from shelljob import proc
import subprocess
import os

app = Flask(__name__)

debut = False

value = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute')
def execute():
    global value
    value = request.args.get('value')
    print("execution du stream et de l'actualisation de la valeur",value)
    # value correspond à la valeur du slider
    #subprocess.run(["python3", "main.py", '-value', str(value)])
    #g = proc.Group()
    print("actualisation de la carte")
    return jsonify({'reload': True})

@app.route('/iframe')
def iframe():
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)
