from flask import Flask

from flask_cors import CORS

from application.rest import scantron

def create_app(config_name):
    
    app = Flask(__name__)

    @app.route('/api/data', methods=['GET'])
    def get_data():
        return jsonify({'message': 'Hello from Flask!'})
         
    config_module = f"application.config.{config_name.capitalize()}Config"

    app.config.from_object(config_module)

    app.register_blueprint(scantron.blueprint)
    
    CORS(app)

    return app
