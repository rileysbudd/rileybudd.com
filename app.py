from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('quote.html')

@app.route('/dumbquote')
def dumbquote():
    return render_template('quote.html')

if __name__ == "__main__":
    app.run()