from flask import Flask
from routes.auth_routes import auth_bp
from routes.tasks_routes import tasks_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


app.register_blueprint(tasks_bp, url_prefix='/tasks')
app.register_blueprint(auth_bp, url_prefix='/auth')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=os.getenv("PORT"))     