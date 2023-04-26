from flask import Flask, render_template
import subprocess
from flask import request

app = Flask(__name__)

with open('diff_jours.txt','w') as f:
    f.write("0")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iframe')
def iframe():
    return render_template('map.html')

@app.route('/execute')
def execute():
    value = request.args.get('value')
    print('execution')
    # Execute Python script with value as parameter
    subprocess.call(['python3', 'cartographie.py', value])
    
    # Render a new template that includes the additional element
    return ''

if __name__ == '__main__':
    app.run(debug=True)
