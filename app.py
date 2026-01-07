from flask import Flask, request, render_template, current_app, jsonify
# from config import config
import funcs
from classes import ShopifyIntegration


app = Flask(__name__)

@app.route('/')
def homepage():
    base_url = request.url_root.rstrip('/')
    return render_template('home.html.j2', base_url=base_url)

@app.route('/sprite_spacer')
def sprite_spacer():
    base_url = request.url_root.rstrip('/')
    return render_template('sprite_spacer.html.j2', base_url=base_url)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return render_template('chat.html.j2')

    # POST request
    data = request.get_json()
    user_message = data.get('message', '')

    # Your chatbot logic here
    response = f"You said: {user_message}"

    return jsonify({'response': response})


#This just serves content from the static folder, where filepath is starts from within /static/
@app.route('/static/<filepath>')
def send_static_file(filepath):
    return current_app.send_static_file(filepath)
    # return filepath

# @app.route('/firestore/connected')
# def verify_firestore_connection():
#     testing_doc_001_ref = config.clients.firestore.collection("testing").document("001")
#     doc = testing_doc_001_ref.get()
#     if doc.exists:
#         return doc.get('confirmation')
#     else:
#         return "Oh no! You're disconnected."


# @app.route('/bucket/<filepath>')
# def gcp_bucket(filepath):
#     blob = config.clients.bucket.blob(filepath)
#     if blob.exists():
#         return blob.download_as_bytes(), 200, {
#             'Content-Type': blob.content_type,
#             'Content-Disposition': 'inline'
#         }
#     else:
#         return 'Object not found', 404


#This uses openai to generate a dumb quote that can be loaded through an iframe
# @app.route('/dumbquote')
# def dumbquote():
#     quote, author = funcs.generate_dumbquote()
#     return render_template('quote.html', quote=quote, author=author)


#This uses openai to generate an icebreaker that can be loaded through an iframe
# @app.route('/icebreaker')
# def icebreaker():
#     icebreaker = funcs.generate_icebreaker()
#     return render_template('question.html', question=icebreaker)


# @app.route('/shopify/<store_id>/google_shopping_feed.xml')
# def get_products(store_id):
#     store = ShopifyIntegration(store_id)
#     store_data = {
#         "name": "My Store Name",
#         "url": "https://mystorename.com"
#     }
#     # Render XML with Jinja2 template
#     return render_template('google_shopping_feed.xml.j2', items=store.feed, store=store_data), {'Content-Type': 'application/xml'}
#     # return store.feed


# @app.route('/google_shopping_feed.xml')
# def product_feed():
#     store = {
#         "name": "My Store Name",
#         "url": "https://mystorename.com"
#     }
#     products = [
#         {
#             "id": "1",
#             "title": "Product One",
#             "description": "Description for Product One",
#             "price": "29.99",
#             "main_sku": "P001",
#             "variant_sku": "V001",
#             "variants": [
#                 {"id": "101", "title": "Variant One", "price": "29.99", "sku": "V001"},
#                 {"id": "102", "title": "Variant Two", "price": "34.99", "sku": "V002"}
#             ]
#         },
#         {
#             "id": "2",
#             "title": "Product Two",
#             "structured_description": {
#                 "content": "This is a structured description for product 2",
#                 "digital_source_type": "trained_algorithmic_media"
#             },
#             "price": "49.99",
#             "main_sku": "P002"
#         },
#         {
#             "id": "2",
#             "structured_title": {
#                 "content": "Product 3",
#                 "digital_source_type": "trained_algorithmic_media"
#             },
#             # "description": "Description for Product Two",
#             "price": "59.99",
#             "sku": "P003",
#             "additional_image_links": [
#                 "https://example.com/additional_image_1",
#                 "https://example.com/additional_image_2"
#             ]
#         }
#     ]


#     # Render XML with Jinja2 template
#     return render_template('google_shopping_feed.xml.j2', items=products, store=store), {'Content-Type': 'application/xml'}


@app.route('/invoice')
def invoice():
    return render_template('invoice.html.j2')

@app.route('/invoice2')
def invoice2():
    invoice_number = '348971-000002'

    dates = {
        'created': 'October 3, 2024',
        'due': 'October 4, 2024'
    }

    client = {
        'company': 'Digital Will Ads',
        'contact': {
            'name': 'Stacey Fielding',
            'email': 'finance@digitalwillads.com'
        }
    }

    items = [
        {
            'date': 'September 16, 2024',
            'quantity': 1.5,
            'rate': 50,
            'description': 'Google Ad campaign buildouts for Perspire TV'
        },{
            'date': 'September 17, 2024',
            'quantity': 2,
            'rate': 50,
            'description': 'Negative keyword filtering for Perspite TV. Analyzing Google and Hubspot accounts for Atlantic Training'
        },{
            'date': 'September 18, 2024',
            'quantity': 2,
            'rate': 50,
            'description': 'Client communications with Atlantic Training. Ad account check-in for Perspire TV and weekly update. Some housekeeping items.'
        },{
            'date': 'September 19, 2024',
            'quantity': 4.25,
            'rate': 50,
            'description': 'Account anlysis for DefinIT, creating new ads. Keyword analysis and campaign buildout for Atlantic Training.'
        },{
            'date': 'September 20, 2024',
            'quantity': 4.25,
            'rate': 50,
            'description': 'Atlantic Training Google Ad campaign buildouts.'
        },{
            'date': 'September 23, 2024',
            'quantity': 1,
            'rate': 50,
            'description': 'Clickup check-in, housekeeping, communication.'
        },{
            'date': 'September 24, 2024',
            'quantity': 0.5,
            'rate': 50,
            'description': 'Atlantic training Google Ad campaign buildouts.'
        },{
            'date': 'September 25, 2024',
            'quantity': 1.5,
            'rate': 50,
            'description': 'Atlantic Training client communication, checking in on the ad account, confirming strategic direction with client. Troubleshooting with the Zapier integration for Google Ad tracking.'
        },{
            'date': 'September 26, 2024',
            'quantity': 0.5,
            'rate': 50,
            'description': 'Updating Perspire TV and Atlantic Training.'
        }
    ]

    return render_template('invoice2.html.j2', items = items, dates=dates, invoice_number=invoice_number, client=client)
# Dope site for templates:https://html5up.net/
# Invoice template https://codepen.io/pvanfas/pen/vYEmGmK


@app.route('/connect')
def connect():
    return render_template('calendly.html')

if __name__ == "__main__":
    app.run()

