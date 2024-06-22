import logging
from flask import Flask, jsonify
from routes import app as routes_app
from database import init_db

app = Flask(__name__)
app.register_blueprint(routes_app)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Error: {str(e)}")
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
