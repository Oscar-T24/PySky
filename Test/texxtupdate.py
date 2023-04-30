from flask import Flask, render_template

app = Flask(__name__)

# Route to serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')

# Route to serve the text file
@app.route('/text')
def text():
    with open('text.txt', 'r') as f:
        return f.read()

if __name__ == '__main__':
    app.run()