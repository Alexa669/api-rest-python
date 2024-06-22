from flask import Flask
from routes import app as routes_app
from database import init_db

app = Flask(__name__)
app.register_blueprint(routes_app)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
