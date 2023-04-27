import flask
from flask import Flask, render_template, request, Response
from shelljob import proc

app = Flask(__name__)

with open('diff_jours.txt', 'w') as f:
    f.write("0")

def read_process(value='0'):
    g = proc.Group()
    p = g.run(["python3", "main.py", '-value', value])
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
    value = request.args.get('value')
    print("execution du stream et de l'actualisation de la valeur")
    return Response(read_process(value), mimetype='text/plain')


if __name__ == '__main__':
    app.run(debug=True)
