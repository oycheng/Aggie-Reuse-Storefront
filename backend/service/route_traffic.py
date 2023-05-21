from flask import Flask, request, Blueprint, jsonify
import json
import logging
from .databaseFunction import *
from config import databaseName, location


bp = Blueprint('traffic', __name__)
# logging.debug(' log message')


# route for get the traffic in some time period
@bp.route('/traffic', methods=['GET'])
def traffic_get():
    # database function ======================================

    # database function ======================================
    return "traffic input recived and processed"


# route for update the traffic in some time period
@bp.route('/traffic', methods=['POST'])
def traffic_post():
    try:
        # database function ======================================

        response_data = {'message': 'traffic POST request executed'}
        return jsonify(response_data)

    # exception
    except KeyError as e:
        # Handle missing field error
        return f'Missing field error: {e}', 400
    except Exception as e:
        # Handle other exceptions
        return f'Internal server error: {e}', 500