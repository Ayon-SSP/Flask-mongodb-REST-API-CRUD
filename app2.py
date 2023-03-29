# Not configured the mongoDB with flask app: I have not configured the mongoDB with flask app.

from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# MongoDB Configuration
client = MongoClient('mongodb://localhost:27017/mydb2')
db = client['mydb2']
users_collection = db['users']


class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password
        }


@app.route('/users', methods=['GET'])
def get_users():
    users = [user for user in users_collection.find({}, {'_id': 0})]
    return jsonify(users)


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users_collection.find_one({'_id': ObjectId(user_id)}, {'_id': 0})
    return jsonify(user)


@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.json
    user = User(user_data['name'], user_data['email'], user_data['password'])
    user_id = users_collection.insert_one(user.to_dict()).inserted_id
    return jsonify(str(user_id))


@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.json
    updated_user = User(user_data['name'], user_data['email'], user_data['password'])
    users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': updated_user.to_dict()})
    return jsonify('User updated')


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    users_collection.delete_one({'_id': ObjectId(user_id)})
    return jsonify('User deleted')


if __name__ == '__main__':
    app.run(debug=True)