import flask
from flask import Flask, render_template, request, Response, make_response,redirect
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=str, help='the port number')
args = parser.parse_args()

if not hasattr(args, 'port') or not args.port: # si aucun argument n'est passé à l'execution du script
    port = '5000'
    print('port not defined')
else:
    port = args.port # recuperer le string du port

# Rest of your code using the port variable



app = Flask(__name__) # instantiation d'un objet de la classe Flask pour émuler une page 
debut = False

value = 0
with open('templates/actu.txt','w') as f:
    f.write('')

@app.route('/') # ouvrir un domaine principal qui utilisera index.html (dans le dossier Templates)
def index():
    print('retour au site principal','port :',port)
    #with open('templates/actu.txt','w') as f:
       #f.write('')
    lien_iframe = f'http://93.14.22.225:{port}/iframe'
    return render_template('index.html',updated=False,lien_iframe=lien_iframe)

@app.route('/execute') # ouvrir un sous domaine /execute qui sera utilisé pour actualiser la carte
# il prendra un argument avec la methode GET nomme value
# exemple de requette utilisateur pour actualiser le site : (console js) fetch('/execute?value=0'); qui actualisera la carte pour le jour d'aujourdhui
def execute():
    global value 
    value = request.args.get('value')
    print("execution du stream et de l'actualisation de la valeur",value)
    '''
    if value == None:
        with open('fichier_temp.txt','r') as f:
            value = f.read()
        print('execution de main.py')
        subprocess.run(["python3", "main.py", '-value', str(value)])
        print('main.py executé')
        with open('templates/actu.txt','a') as f:
            f.write('actualiser')
    else:
        
        with open('fichier_temp.txt','w') as f:
            f.write(value)
    '''
    if value != None :
        subprocess.run(["python3", "main.py", '-value', str(value)])
        with open('templates/actu.txt','a') as f:
            f.write('actualiser')
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

@app.after_request
def add_favicon(response):
    favicon_html = '<link rel="icon" type="image/x-icon" href="http://93.14.22.225/favicon.ico">'
    response.data = response.data.replace(b'</head>', favicon_html.encode() + b'</head>')
    return response

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=port) # lancer l'app en boucle et activer le debogage en initialisation
