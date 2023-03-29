from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)
api = Api(app)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'
mongo = PyMongo(app)

class User(Resource):
    def get(self, id=None):
        if id:
            try:
                user = mongo.db.users.find_one({'id': id})
                if user:
                    return {'_id': str(user['_id']), 'id': user['id'], 'name': user['name'], 'email': user['email'], 'password': user['password']}
                else:
                    return {'error': 'User not found'}, 404
            except:
                return {'error': 'Invalid id'}, 400
        else:
            users = []
            for user in mongo.db.users.find():
                users.append({'_id': str(user['_id']), 'id': user['id'], 'name': user['name'], 'email': user['email'], 'password': user['password']})
            return users

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, help='id cannot be blank')
        parser.add_argument('name', required=True, help='name cannot be blank')
        parser.add_argument('email', required=True, help='email cannot be blank')
        parser.add_argument('password', required=True, help='password cannot be blank')
        args = parser.parse_args()

        user = mongo.db.users.find_one({'id': args['id']})
        if user:
            return {'error': 'User already exists'}, 409

        mongo.db.users.insert_one({'id': args['id'], 'name': args['name'], 'email': args['email'], 'password': args['password']})
        return {'message': 'User created successfully'}, 201

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='name cannot be blank')
        parser.add_argument('email', required=True, help='email cannot be blank')
        parser.add_argument('password', required=True, help='password cannot be blank')
        args = parser.parse_args()

        user = mongo.db.users.find_one({'id': id})
        if user:
            mongo.db.users.update_one({'id': id}, {'$set': {'name': args['name'], 'email': args['email'], 'password': args['password']}})
            return {'message': 'User updated successfully'}, 200
        else:
            return {'error': 'User not found'}, 404

    def delete(self, id):
        user = mongo.db.users.find_one({'id': id})
        if user:
            mongo.db.users.delete_one({'id': id})
            return {'message': 'User deleted successfully'}, 200
        else:
            return {'error': 'User not found'}, 404

api.add_resource(User, '/users', '/users/<string:id>')

if __name__ == '__main__':
    app.run(debug=True)
