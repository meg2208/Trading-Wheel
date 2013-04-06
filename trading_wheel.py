
from flask import Flask, render_template, flash

app = Flask(__name__)
app.config.from_object('flask_settings')

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
