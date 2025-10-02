Here’s a step-by-step guide to communicate with **MongoDB using Flask and PyMongo**, and how to perform **CRUD operations** (Create, Read, Update, Delete):

---

## 📦 1. Install Required Packages

```bash
pip install flask pymongo dnspython
```

> `dnspython` is needed if you use a MongoDB Atlas connection string.

---

## 📁 2. Project Structure

```
flask_mongo_app/
│
├── app.py
└── requirements.txt
```

---

## ⚙️ 3. Basic Flask + PyMongo Setup

### `app.py`

```python
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# ✅ MongoDB connection (local or Atlas)
app.config["MONGO_URI"] = "mongodb://localhost:27017/flaskdb"
client = MongoClient(app.config["MONGO_URI"])

db = client["flaskdb"]
collection = db["users"]

# Home route
@app.route("/")
def home():
    return "Flask + MongoDB is running!"

```

---

## ➕ 4. Create (Insert Data)

```python
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    user_id = collection.insert_one({
        "name": data.get("name"),
        "email": data.get("email"),
        "age": data.get("age")
    }).inserted_id

    return jsonify({"message": "User created", "id": str(user_id)}), 201
```

👉 **Test with cURL or Postman**

```bash
curl -X POST http://127.0.0.1:5000/users \
-H "Content-Type: application/json" \
-d '{"name":"Mouad","email":"mouad@example.com","age":25}'
```

---

## 📥 5. Read (Get Data)

### Get all users

```python
@app.route("/users", methods=["GET"])
def get_users():
    users = []
    for user in collection.find():
        user["_id"] = str(user["_id"])
        users.append(user)
    return jsonify(users)
```

### Get single user by ID

```python
@app.route("/users/<id>", methods=["GET"])
def get_user(id):
    user = collection.find_one({"_id": ObjectId(id)})
    if user:
        user["_id"] = str(user["_id"])
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404
```

---

## ✏️ 6. Update

```python
@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    data = request.get_json()
    result = collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": data}
    )
    if result.matched_count == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User updated"})
```

---

## 🗑️ 7. Delete

```python
@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User deleted"})
```

---

## 🚀 8. Run the App

```bash
export FLASK_APP=app.py
flask run
```

Or simply:

```bash
python app.py
```

---

## 📌 9. Notes & Best Practices

* Use **environment variables** for sensitive data (e.g., MongoDB URI).
* For production, consider using [Flask-PyMongo](https://flask-pymongo.readthedocs.io/) or an ODM like **MongoEngine**.
* Add error handling and validation (e.g., with `marshmallow` or `pydantic`).
* If deploying (e.g., on Railway/Render), ensure MongoDB URI is configured in `.env`.

---

### ✅ Example `.env`

```
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/myDatabase
```

---

Would you like me to extend this example to use **Blueprints + MVC structure** for a more scalable project?
