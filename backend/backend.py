from flask import Flask
from service.route_store import bp as store_bp
from service.route_traffic import bp as traffic_bp


app = Flask(__name__)

# Register the routes Blueprints
app.register_blueprint(store_bp)
app.register_blueprint(traffic_bp)

# Run the application
if __name__ == '__main__':
    app.run()