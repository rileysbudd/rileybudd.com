from flask import Flask, request, render_template, current_app
from config import config
import funcs


app = Flask(__name__)


#This just serves content from the static folder, where filepath is starts from within /static/
@app.route('/static/<filepath>')
def send_static_file(filepath):
    return current_app.send_static_file(filepath)
    # return filepath



#This uses openai to generate a dumb quote that can be loaded through an iframe
@app.route('/dumbquote')
def dumbquote():
    quote, author = funcs.generate_dumbquote()
    return render_template('quote.html', quote=quote, author=author)

#This uses openai to generate an icebreaker that can be loaded through an iframe
@app.route('/icebreaker')
def icebreaker():
    icebreaker = funcs.generate_icebreaker()
    return render_template('question.html', question=icebreaker)


@app.route('/google_shopping_feed.xml')
def product_feed():
    store = {
        "name": "My Store Name",
        "url": "https://mystorename.com"
    }
    products = [
        {
            "id": "1",
            "title": "Product One",
            "description": "Description for Product One",
            "price": "29.99",
            "main_sku": "P001",
            "variant_sku": "V001",
            "variants": [
                {"id": "101", "title": "Variant One", "price": "29.99", "sku": "V001"},
                {"id": "102", "title": "Variant Two", "price": "34.99", "sku": "V002"}
            ]
        },
        {
            "id": "2",
            "title": "Product Two",
            "structured_description": {
                "content": "This is a structured description for product 2",
                "digital_source_type": "trained_algorithmic_media"
            },
            "price": "49.99",
            "main_sku": "P002"
        },
        {
            "id": "2",
            "structured_title": {
                "content": "Product 3",
                "digital_source_type": "trained_algorithmic_media"
            },
            # "description": "Description for Product Two",
            "price": "59.99",
            "sku": "P003",
            "additional_image_links": [
                "https://example.com/additional_image_1",
                "https://example.com/additional_image_2"
            ]
        }
    ]

    # Render XML with Jinja2 template
    return render_template('google_shopping_feed.xml.j2', products=products, store=store), {'Content-Type': 'application/xml'}



if __name__ == "__main__":
    app.run()

