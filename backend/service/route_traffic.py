from flask import Flask, request, Blueprint, jsonify
import json
import logging
from .databaseFunction import *

bp = Blueprint('traffic', __name__)
# logging.debug(' log message')


# route for get the traffic in some time period
@bp.route('/traffic', methods=['GET'])
def traffic_get():
    try:
        json_payload = request.get_json()
        time = json_payload["time"]

        # Handle GET request

        # body
        #
        #
        #
        #

        response_data = {'message': 'traffic GET request received'}
        return jsonify(response_data)

    # exception
    except KeyError as e:
        # Handle missing field error
        return f'Missing field error: {e}', 400
    except Exception as e:
        # Handle other exceptions
        return f'Internal server error: {e}', 500


# route for update the traffic in some time period
@bp.route('/traffic', methods=['POST'])
def traffic_post():
    try:
        json_payload = request.get_json()
        time = json_payload["time"]

        # Handle GET request

        # body
        #
        #
        #
        #

        response_data = {'message': 'traffic POST request received'}
        return jsonify(response_data)

    # exception
    except KeyError as e:
        # Handle missing field error
        return f'Missing field error: {e}', 400
    except Exception as e:
        # Handle other exceptions
        return f'Internal server error: {e}', 500