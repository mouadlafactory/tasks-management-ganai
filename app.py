from flask import Flask
from routes.auth_routes import auth_bp
from routes.tasks_routes import tasks_bp
from routes.web_routes import web_bp
from dotenv import load_dotenv
from mongoengine import connect

import os

load_dotenv()   

app = Flask(__name__)

# Register blueprints
app.register_blueprint(web_bp)  # Web routes (no prefix for root routes)
app.register_blueprint(tasks_bp, url_prefix='/tasks')
app.register_blueprint(auth_bp, url_prefix='/auth')



if __name__ == '__main__':
    try:
        # Connect to MongoDB
        mongo_uri = os.getenv('MONGO_DB_URI', 'mongodb://localhost:27017/')
        connect(
            db='task_manager',  # Database name as first parameter
            host=mongo_uri,
        )
        print(f"Connected to MongoDB: task_manager ✅")
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        print("Note: Make sure MongoDB is running on your system")
   
    port = int(os.getenv("PORT", 8080))
    print(f"🚀 Starting Flask app on port {port}  ❇️")
    app.run(host="0.0.0.0", debug=True, port=port)     