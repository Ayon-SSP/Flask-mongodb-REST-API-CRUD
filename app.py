from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.secret_key = "secretkey"

    app.config['MONGO_URI'] = "mongodb://localhost:27017/mydb"

mongo = PyMongo(app)




@app.route('/users',methods=['POST'])
def create_user():
    currentCollection = mongo.db.users
    _json = request.json
    id = _json['id']
    name = _json['name']
    email = _json['email']
    password = _json['password']
    if name and email and password and request.method == "POST":
        # _hashed_password = generate_password_hash(password)
        _hashed_password = generate_password_hash(password)
        id = currentCollection.insert_one({'name':name,'email':email,'password':_hashed_password})
        resp = jsonify("User Added successfully")
        resp.status_code = 200
        return resp







if __name__ == "__main__":
    app.run(debug=True)