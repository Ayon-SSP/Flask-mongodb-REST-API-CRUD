from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)

# MongoDB Configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydb2'
mongo = PyMongo(app)


class User:
    def __init__(self, id=None, name=None, email=None, password=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            '_id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password
        }

    @classmethod
    def from_dict(cls, user_dict):
        return cls(
            id=user_dict.get('_id'),
            name=user_dict.get('name'),
            email=user_dict.get('email'),
            password=user_dict.get('password')
        )

    def save(self):
        user_data = self.to_dict()
        if self.id:
            mongo.db.users.update_one({'_id': ObjectId(self.id)}, {'$set': user_data})
        else:
            self.id = str(mongo.db.users.insert_one(user_data).inserted_id)

    def delete(self):
        mongo.db.users.delete_one({'_id': ObjectId(self.id)})

    @classmethod
    def find_all(cls):
        users = [cls.from_dict(user_dict) for user_dict in mongo.db.users.find()]
        return users

    @classmethod
    def find_by_id(cls, user_id):
        user_dict = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if user_dict:
            return cls.from_dict(user_dict)

    def update(self, user_dict):
        self.name = user_dict.get('name', self.name)
        self.email = user_dict.get('email', self.email)
        self.password = user_dict.get('password', self.password)
        self.save()


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        users = [user.to_dict() for user in User.find_all()]
        return jsonify(users)
    elif request.method == 'POST':
        user_data = request.json
        user = User.from_dict(user_data)
        user.save()
        return jsonify(user.id)


@app.route('/users/<string:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user(user_id):
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'PUT':
        user_data = request.json
        user.update(user_data)
        return jsonify({'message': 'User updated'})
    elif request.method == 'DELETE':
        user.delete()
        return jsonify({'message': 'User deleted'})


if __name__ == '__main__':
    app.run(debug=True)
