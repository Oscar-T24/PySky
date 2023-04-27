import flask
from flask import Flask, render_template, request, Response
from shelljob import proc

app = Flask(__name__)

debut = False

value = 0

def generate(g,value):
    print('generation avec',value)
    p = g.run(["python3", "main.py", '-value', str(value)])
    while g.is_pending():
        lines = g.readlines()
        for proc, line in lines:
            yield line

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iframe')
def iframe():
    return render_template('map.html')

@app.route('/execute')
def execute():
    global value
    value = request.args.get('value')
    print("execution du stream et de l'actualisation de la valeur",value)
    g = proc.Group()
    return flask.Response(flask.stream_with_context(generate(g,value)), mimetype='text/plain')

@app.route('/stream')
def read_process():
    global value
    print('valeur recue :', value)
    g = proc.Group()
    return flask.Response(flask.stream_with_context(generate(g,value)), mimetype='text/plain')
    
if __name__ == '__main__':
    app.run(debug=True)
