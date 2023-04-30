import flask
from flask import Flask, render_template, request, Response

app = Flask(__name__)

with open('diff_jours.txt', 'w') as f:
    f.write("0")

@app.route('/stream')
def read_process(value='0'):
        print('valeur recue :',value)
        from shelljob import proc
        g = proc.Group()
        p = g.run(["python3", "main.py", '-value', value])
        while g.is_pending():
            lines = g.readlines()
            for proc, line in lines:
                yield line
    '''
    def read_process(value='0'):
    print('valeur recue :', value)
    from shelljob import proc
    g = proc.Group()
    p = g.run(["python3", "main.py", '-value', value])
    def generate():
        while g.is_pending():
            lines = g.readlines()
            for proc, line in lines:
                yield line
    return flask.Response(flask.stream_with_context(generate()), mimetype='text/plain')
    '''
    

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/iframe')
def iframe():
    return render_template('map.html')


@app.route('/execute')
def execute():
    value = request.args.get('value')
    print("execution du stream et de l'actualisation de la valeur",value)
    return flask.Response(flask.stream_with_context(generate()), mimetype='text/plain')


if __name__ == '__main__':
    app.run(debug=True)
