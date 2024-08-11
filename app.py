from flask import Flask, render_template
from config import config
import funcs

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World!"

@app.route('/dumbquote')
def dumbquote():
    quote, author = funcs.generate_dumbquote()
    return render_template('quote.html', quote=quote, author=author)

@app.route('/icebreaker')
def icebreaker():
    icebreaker = funcs.generate_icebreaker()
    return render_template('question.html', question=icebreaker)

if __name__ == "__main__":
    app.run()

