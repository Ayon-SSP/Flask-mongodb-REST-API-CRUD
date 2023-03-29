# configured the mongoDB with flask app: I have configured the mongoDB with flask app.
# I have used the flask_pymongo library to connect to the database.
# I have created a class User to store the user data.
# I have created the following routes to perform CRUD operations on the users collection.

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)

# MongoDB Configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydb2'
mongo = PyMongo(app)

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
    users = [User(user['name'], user['email'], user['password']).to_dict() for user in mongo.db.users.find()]
    return jsonify(users)


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    # user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    user = User(mongo.db.users.find_one({'_id': ObjectId(user_id)})['name'],
                mongo.db.users.find_one({'_id': ObjectId(user_id)})['email'],
                mongo.db.users.find_one({'_id': ObjectId(user_id)})['password']).to_dict()
    return jsonify(user)


@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.json
    user = User(user_data['name'], user_data['email'], user_data['password'])
    user_id = mongo.db.users.insert_one(user.to_dict()).inserted_id
    return jsonify(str(user_id))


@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.json
    updated_user = User(user_data['name'], user_data['email'], user_data['password'])
    mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': updated_user.to_dict()})
    return jsonify('User updated')


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    mongo.db.users.delete_one({'_id': ObjectId(user_id)})
    return jsonify('User deleted')


if __name__ == '__main__':
    app.run(debug=True)
