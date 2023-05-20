from flask import Flask, request, jsonify
import json
from databaseAccess import Store

app = Flask(__name__)

# Define a route and handler for handling requests
@app.route('/api/store', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'GET':
        # Handle GET request
        data = {'message': 'GET request received'}
        return jsonify(data)
    elif request.method == 'POST':
        # Handle POST request
        request_data = request.get_json()
        # Process the request data
        # ...


        response_data = {'message': 'POST request received', 'data': request_data}
        return jsonify(response_data)


@app.route('/api/store/reserve', methods=['PUT'])
def reserve():
    try:
        # Get the JSON payload from the request
        json_payload = request.get_json()

        # Access the fields from the JSON payload
        data = json_payload["number"]

        returnData = {'message': 'PUT request received', 'body': 'Want to reserve', 'gotNum': data}
        return jsonify(returnData)
    except KeyError as e:
        # Handle missing field error
        return f'Missing field error: {e}', 400
    except Exception as e:
        # Handle other exceptions
        return f'Internal server error: {e}', 500

if __name__ == '__main__':
    app.run()