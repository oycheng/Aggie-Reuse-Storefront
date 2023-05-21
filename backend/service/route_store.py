from flask import Flask, request, Blueprint, jsonify
import json
import logging
from .databaseFunction import *
from config import databaseName, location


bp = Blueprint('store', __name__)
# logging.debug(' log message')


# route for store inventory managment
@bp.route('/store/Items', methods=['GET'])
def storeItems_get():
    try:
        json_payload = request.get_json()

        # unpack the request
        startIndex = json_payload["Start"]
        endIndex = json_payload["End"]
        getTags = json_payload["TotalTags"]
        getPages = json_payload["TotalPages"]
        selectTag = json_payload["SelectTag"]


        # Handle GET request
        response_data = get_items(startIndex, endIndex, getTags, getPages, selectTag)
        return jsonify(response_data)
    # exception
    except KeyError as e:
        # Handle missing field error
        return f'Missing field error: {e}', 400
    except Exception as e:
        # Handle other exceptions
        return f'Internal server error: {e}', 500

# route add a image of item to database
@bp.route('/store/Items', methods=['POST'])
def storeItems_post():
    if 'image' in request.files:
        image = request.files['image']
        tags = request.form.get('tags')
        response = add_items(image, tags)
        
        if (response == 'success'):
            return 'Image uploaded successfully.'
        else:
            return 'Faild to upload Image.'

    return 'No image file found in the request.'

# Add Barcode to database
@bp.route('/store', methods=['POST'])
def store_post():
    try:
        json_payload = request.get_json()
        barcode = json_payload["barcode"]
        
        # Handle POST request
        store(databaseName, location, barcode)

        response_data = {'message': 'POST request executed', 'barcode': barcode}
        return jsonify(response_data)

    # exception
    except KeyError as e:
        # Handle missing field error
        return f'Missing field error: {e}', 400
    except Exception as e:
        # Handle other exceptions
        return f'Internal server error: {e}', 500


# Put a Reservation
@bp.route('/store/reserve', methods=['PUT'])
def reserve():
    try:
        # Get the JSON payload from the request
        json_payload = request.get_json()

        # Access the fields from the JSON payload
        barcode = json_payload["barcode"]

        # body
        #
        #
        #
        #

        returnData = {'message': 'Item reserved', 'barcode': barcode}
        return jsonify(returnData)
        
    # exception
    except KeyError as e:
        # Handle missing field error
        return f'Missing field error: {e}', 400
    except Exception as e:
        # Handle other exceptions
        return f'Internal server error: {e}', 500

# Cancel Reservation
@bp.route('/store/reserve', methods=['DELETE'])
def cancleReserve():
    try:
        # Get the JSON payload from the request
        json_payload = request.get_json()

        # Access the fields from the JSON payload
        barcode = json_payload["barcode"]

        # body
        #
        #
        #
        #

        returnData = {'message': 'Reservation canceled', 'barcode': barcode}
        return jsonify(returnData)
        
    # exception
    except KeyError as e:
        # Handle missing field error
        return f'Missing field error: {e}', 400
    except Exception as e:
        # Handle other exceptions
        return f'Internal server error: {e}', 500