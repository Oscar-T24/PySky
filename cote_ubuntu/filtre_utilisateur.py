from flask import Flask, request, redirect, render_template,url_for
import re
import docker
import requests
import re
import subprocess
import string
import random
import re
import time
import json

app = Flask(__name__)

def generer_cle(taille,port):
    cle = []
    assert taille % 2 == 0, 'vauillez entrer une taille paire'
    for i in range(0,taille,2):
        cle += random.choice(string.ascii_lowercase)
        if ord(cle[i]) % 3 == 0:
            cle[i] = cle[i].upper()
        cle.append(str(ord(cle[i])+4))
        longueur_ini = len(cle)
    for i in range(4):
        #print(cle)
        cle.insert(longueur_ini//4*i,'-'+chr(int(port[i])+32))
        print("insertion à l'indice",longueur_ini//4*i)
    return "".join(cle)


def update_nginx_conf(backend_port):
    # Modify the backend_port in the nginx.conf file
    #with open('/etc/nginx/nginx.conf', 'r') as file:
        #nginx_conf = file.read()
    
    # Use regular expression to find and replace the port value
    #nginx_conf = re.sub(r'set \$backend_port \d+;', f'set $backend_port {backend_port};', nginx_conf)
    
    #with open('/etc/nginx/nginx.conf', 'w') as file:
       # file.write(nginx_conf)
    
    # Restart Nginx
    #subprocess.run(['sudo', 'systemctl', 'restart', 'nginx'], check=True)
    pass

def get_container_id_by_port(port):
    client = docker.from_env()
    containers = client.containers.list()
    for container in containers:
        container_ports = container.attrs['NetworkSettings']['Ports']
        for container_port in container_ports:
            if container_ports[container_port] is not None:
                host_port = container_ports[container_port][0]['HostPort']
                if host_port == port:
                    return container.id
    return None

def remove_escapes(logs):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', logs)

@app.route('/')
def index():
    print('retour page principale')
    # request.access_route = L'IP DU CLIENT
    print(request.blueprint)
    print(request.origin)
    return render_template('index.html')

@app.route('/set_port', methods=['POST'])
def set_port():
    backend_port = request.form['backend_port']
    user_name = request.form['user_name']
    # AJOUTER USER NAME AU DOCKER
    
    # Update the backend_port in the nginx.conf file and restart Nginx
    update_nginx_conf(backend_port)
    
    # Do whatever you want with the backend_port value
    print(f"Backend Port: {backend_port}")

    docker_command = f'sudo docker run -d -p {backend_port}:{backend_port} -e PORT={backend_port} --name {user_name} app'
    try:
        command = "sudo docker container ls --format '{{.Names}}'"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout.strip()  # Get the command output
    
        # noms : utilisateurs
        container_names = output.split("\n")

        command = "sudo docker container ls --format '{{.Ports}}'"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output2 = result.stdout.strip()  # Get the command output

        container_ports = output2.split("\n") # separation par utilisateur
        for i in range(len(container_ports)):
            container_ports[i] = container_ports[i][container_ports[i].index(':')+1:container_ports[i].index('->')]
        time.sleep(1)
        cle =  generer_cle(14,backend_port)
        # SI L'UTILISATEUR EXISTE DEJA
        if user_name in container_names:
            if container_ports[container_names.index(user_name)] == backend_port:
                return f'''
                <html>
                    <meta http-equiv="refresh" content="5;url=http://93.14.22.225:{backend_port}?message={cle}/">
                    <body><h1> Re-bonjour, {user_name}</h1><br><h3>redirection</h3><br><h2>{container_ports[container_names.index(user_name)]}</h2></body>
                </html>
                '''
            else:
                return f'''
                <html>
                    <meta http-equiv="refresh" content="5;url=http://93.14.22.225:1025/">
                    <body><h1> Re-bonjour, {user_name}</h1><br><h3>Veuillez rentrer votre port assigné <br>(vous ne pouvez avoir qu'un seul port par utilisateur)</h3></body>
                </html>
                '''

        
        subprocess.run(docker_command, shell=True,check=True)
        print("Initialisation du container au port indiqué")
    except subprocess.CalledProcessError as e:
        print(f"Port déja ouvert pour un autre container: {e}")
        return '''
        <html>
            <meta http-equiv="refresh" content="2;url=http://93.14.22.225:1025/">
            <body><h1>ERREUR : port déja utilisé par un autre utilisateur ou utilisateur existant mais port inncorrect </h1><br><h3>retour vers la page </h3></body>
        </html>
        '''
    time.sleep(1)
    cle =  generer_cle(14,backend_port)
    return f'''
                <html>
                    <meta http-equiv="refresh" content="5;url=http://93.14.22.225:{backend_port}?message={cle}/">
                    <body><h1> Votre session est prete, {user_name}</h1><br><h3>redirection</h3><br><h2></h2></body>
                </html>
                '''
    #return redirect(f'http://93.14.22.225:{backend_port}', message=cle)
    #return redirect(url_for(f'http://93.14.22.225:{backend_port}', message=cle))
    #return redirect('http://93.14.22.225:81')

@app.route('/show_log', methods=['POST'])
def display_log():
    port = request.form['backend_port']
    id = get_container_id_by_port(port)
    if id is None:
        return '''
        <html>
            <meta http-equiv="refresh" content="5;url=http://93.14.22.225:1025/">
            <body><h1>ERREUR : session inexistante ou introuvable </h1><br><h3>retour vers la page </h3></body>
        </html>
        '''
    client = docker.from_env()
    container = client.containers.get(id)
    logs = container.logs().decode('utf-8')
    log_lines = logs.splitlines()
    logs = remove_escapes(logs)
    final = [line for line in log_lines if 'GET /text' not in line] # enlever les requettes du fichier texte inutiles
    #final = [line+'\n' for line in log_lines if 'GET /text' not in line]
    return final
    return render_template('logs.html', logs=final)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1025)
