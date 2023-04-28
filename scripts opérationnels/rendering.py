import flask
from flask import Flask, render_template, request, Response, jsonify ,after_this_request,url_for,redirect
from shelljob import proc
import subprocess


app = Flask(__name__)

debut = False

value = 0

@app.route('/')
def index():
    return render_template('index.html',updated=False)

@app.route('/execute')
def execute():
    global value 
    value = request.args.get('value')
    print("execution du stream et de l'actualisation de la valeur",value)
    if value == None:
        with open('fichier_temp.txt','r') as f:
            value = f.read()
        print('execution de main.py')
        subprocess.run(["python3", "main.py", '-value', str(value)])
        print(value)
    else:
        with open('fichier_temp.txt','w') as f:
            f.write(value)
    # value correspond à la valeur du slider
    #g = proc.Group()
    print("actualisation de la carte")
    # Register a function to trigger a page reload after the response has been sent
    return redirect('/')#redirect(url_for('execute'))

@app.route('/iframe')
def iframe():
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)
