from flask import Flask
from service.test2 import bp as routes_bp


app = Flask(__name__)

# gloable variable
databaseName = "Invertory"
location = "1"

# Register the routes Blueprints
app.register_blueprint(routes_bp)

# Run the application
if __name__ == '__main__':
    app.run()