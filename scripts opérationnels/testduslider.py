from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

import subprocess
from flask import request

@app.route('/iframe')
def iframe():
    return render_template('map.html')

@app.route('/execute')
def execute():
    value = request.args.get('value')

    # Execute Python script with value as parameter
    subprocess.call(['python3', 'cartographie.py', value])

    return ''

if __name__ == '__main__':
    app.run(debug=True)

