from flask import Flask, render_template
import os

app = Flask(__name__)
app.config['DATA_PATH'] = os.path.join(os.path.dirname(__file__), '../../data')

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)