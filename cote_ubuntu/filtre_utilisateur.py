from flask import Flask, render_template, request,redirect
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_backend_port', methods=['POST'])
def update_backend_port():
    new_port = request.form.get('backend_port')

    # Update Nginx configuration file
    subprocess.run(['sed', '-i', 's/$backend_port {}/$backend_port {};'.format(new_port), '/etc/nginx/nginx.conf'])

    # Reload Nginx to apply the changes
    subprocess.run(['nginx', '-s', 'reload'])

    return redirect("http://93.14.22.225:81", code=302) # rediriger l'utilisateur

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)