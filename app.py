from flask import Flask, request, render_template, current_app
from config import config
import funcs
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

# https://www.geeksforgeeks.org/flask-wtf-explained-how-to-use-it/
class MyForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    country = SelectField('Country', choices=[('IN', 'India'), ('US', 'United States'), ('UK', 'United Kingdom')])

#This just serves content from the static folder
@app.route('/static/<filepath>')
def general(filepath):
    return current_app.send_static_file(filepath)
    # return filepath

@app.route('/test_form')
def test_form():
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        country = form.country.data
        return f"Name: {name} < br > Country: {country}"
    return render_template('form.html', form=form)

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

