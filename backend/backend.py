from flask import Flask
from flask_cors import CORS
from service.route_store import bp as store_bp
from service.route_traffic import bp as traffic_bp


app = Flask(__name__)
CORS(app)

# Register the routes Blueprints
app.register_blueprint(store_bp)
app.register_blueprint(traffic_bp)

# Run the application
if __name__ == '__main__':
    # change host to local IP address for hardware public request
    # app.run(host="172.20.10.3")
    app.run()