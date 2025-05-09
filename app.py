import os
# from pudb import set_trace
from dotenv import load_dotenv
from chome.quickstart import oath #custom package
from googleapi.gmail_SDK_suit import SDK_Suit #custom package
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

load_dotenv()

@app.route('/')
def index():
    # Get default locations for Google Maps
    oathRequest = oath()
    locations = oathRequest.structure_ts()
    
    params = {
        "GOOGLE_MAPS_API_KEY": os.getenv('GOOGLE_MAPS_API_KEY'),
        "locations": locations,
    }
    return render_template('web.html', **params)

# Original Google Maps endpoints (keep for backward compatibility)
@app.route('/v1/endpoint/locations', methods=['POST', 'GET'])
def locq():
    loc = request.form.get('zip')
    limit = 100
    oathRequest = oath()
    locations = oathRequest.structure_ts(zipCode=loc, limit=limit)
    params = {
        "GOOGLE_MAPS_API_KEY": os.getenv('GOOGLE_MAPS_API_KEY'),
        "locations": locations,
    }
    return render_template('locationSearch.html', **params)

@app.route('/api/search', methods=['POST'])
def handle_search():
    data = request.json
    search_term = data.get('searchTerm', '').lower()
    zip_code = data.get('zipCode', '97202')

    kroger = oath()
    stores = kroger.structure_ts(zipCode=zip_code, limit=5)
    if not stores:
        return jsonify({"error": "No stores found"}), 404

    location_id = stores[0]['location_id']
    products = kroger.structure_pos(locationId=location_id, search=search_term)

    formatted_products = []
    for product in products:
        formatted_products.append({
            "name": product.get("name", ""),
            "price": product.get("price", 0),
            "image": product.get("smlImage", ""),
            "store": stores[0]['name'],
            "sku": product.get("productId", ""),
            "stock": 50,
            "category": "",
            "screenshots": product.get("screenshots", [])[3:6]
        })

    return jsonify({
        "products": formatted_products,
        "store": stores[0]['name']
    })

@app.route('/api/stores', methods=['POST'])
def get_stores():
    zip_code = request.json.get('zipCode', '97202')
    kroger = oath()
    stores = kroger.structure_ts(zipCode=zip_code, limit=5)

    formatted_stores = []
    for i, store in enumerate(stores):
        formatted_stores.append({
            "name": store['name'],
            "address": store['address'],
            "distance": f"{i+1} miles",
            "location_id": store['location_id']
        })

    return jsonify({"stores": formatted_stores})

# Original product search endpoints (kept for backward compatibility)
@app.route('/v1/endpoint/products')
def productSearch():
    oathRequest = oath()
    searchResults = oathRequest.structure_pos(search="Shampoo")
    params = {
        "store": "Fred Meyer - Peninsula",
        "items": searchResults,
    }
    return render_template('searchResults.html', **params)

@app.route('/v1/endpoint/productSearch', methods=['POST'])
def productSearchRequest():
    search = request.form.get('search')
    oathRequest = oath()
    searchResults = oathRequest.structure_pos(search=search)
    params = {
        "store": "Fred Meyer - Peninsula",
        "items": searchResults,
    }
    return render_template('searchResults.html', **params)

@app.route('/api/product/aisle', methods=['POST'])
def get_product_aisle():
    data = request.json
    product_id = data.get('productId')
    location_id = data.get('locationId')

    kroger = oath()
    aisle_info = kroger.get_aisle_info_by_id(product_id, location_id)

    if not aisle_info:
        return jsonify({"error": "Aisle information not found"}), 404

    return jsonify(aisle_info)

# Gmail functionality (keep until v2 release)
@app.route('/v1/gmailRequest', methods=['POST'])
def gmailRequests():
    gmail = SDK_Suit()
    itemJSON = request.get_json()
    description = itemJSON.get('description')
    price = itemJSON.get('price')
    image = itemJSON.get('image')

    message_cont = f"""
    <html>
        <head></head>
        <body>
        <img src="{image}">
        <h3>Thank you for your order of <strong style="color: green;">{description}</h3>
        </body>
    </html>
    """
    me = "seymour2@pdx.edu"
    Draft = gmail.create_draft(me, me, 'Order Details Summary', message_cont)
    gmail.send_draft(me, Draft["id"])

    return jsonify({"status": "202"})

if __name__ == '__main__':
    app.run(debug=True)
