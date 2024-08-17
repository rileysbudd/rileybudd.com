from flask import Flask, request, render_template, current_app
from config import config
import funcs

app = Flask(__name__)

#This just serves content from the static folder
@app.route('/static/<filepath>')
def general(filepath):
    return current_app.send_static_file(filepath)
    # return filepath

@app.route('/dumbquote')
def dumbquote():
    quote, author = funcs.generate_dumbquote()
    return render_template('quote.html', quote=quote, author=author)

@app.route('/icebreaker')
def icebreaker():
    icebreaker = funcs.generate_icebreaker()
    return render_template('question.html', question=icebreaker)

#This needs some serious work
@app.route('/images/<dir>/random')
def random_image(dir='examples'):
    if 'quantity' in request.args:
        quantity = int(request.args.get('quantity'))
    else:
        quantity = 1
    images = funcs.random_images(images_dir=dir, quantity=quantity)
    html = ''
    for image in images:
        html += "<img> src='" + image + "'</img>"
    return html

#This is just for testing
@app.route('/query_val')
def query_val():
    if 'key' in request.args:
        value = request.args.get('key')
    else:
        value = "no query 'key'"
    return value

if __name__ == "__main__":
    app.run()

