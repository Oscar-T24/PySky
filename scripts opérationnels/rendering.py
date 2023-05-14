import flask
from flask import Flask, render_template, request, Response, jsonify ,after_this_request,url_for,redirect
import subprocess
from flask_cors import CORS


app = Flask(__name__) # instantiation d'un objet de la classe Flask pour émuler une page 
CORS(app)

debut = False

value = 0
with open('templates/actu.txt','w') as f:
    f.write('')

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response
    
@app.route('/') # ouvrir un domaine principal qui utilisera index.html (dans le dossier Templates)
def index():
    print('retour au site principal')
    #with open('templates/actu.txt','w') as f:
       #f.write('')
    return render_template('index.html',updated=False)

@app.route('/execute') # ouvrir un sous domaine /execute qui sera utilisé pour actualiser la carte
# il prendra un argument avec la methode GET nomme value
# exemple de requette utilisateur pour actualiser le site : (console js) fetch('/execute?value=0'); qui actualisera la carte pour le jour d'aujourdhui
def execute():
    global value 
    value = request.args.get('value') # recuperer la valeur value passée en requette GET dans l'url
    print("execution du stream et de l'actualisation de la valeur",value)
    if value == None:
        with open('fichier_temp.txt','r') as f:
            value = f.read()
        print('execution de main.py')
        subprocess.run(["python3", "main.py", '-value', str(value)]) # executer main.py 
        print('main.py executé')
        with open('templates/actu.txt','a') as f:
            f.write('actualiser')
    else:
        with open('fichier_temp.txt','w') as f:
            f.write(value)
    # value correspond à la valeur du slider
    #g = proc.Group()
    print("actualisation de la carte")
    # Register a function to trigger a page reload after the response has been sent
    return redirect('/')#redirect(url_for('execute'))

@app.route('/iframe') # une autre page qui est generée afin d'afficher la carte (templates/map.html)
def iframe():
    return render_template('map.html')

@app.route('/text')
def text():
    with open('templates/actu.txt', 'r') as f:
        return f.read()

if __name__ == '__main__':
    app.run(debug=True) # lancer l'app en boucle et activer le debogage en initialisation
