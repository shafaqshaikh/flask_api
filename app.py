from flask import Flask , request , jsonify , make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash , check_password_hash
import os
import uuid


app =Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__name__))
#database
app.config['SECRET_KEY']='thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///'+ os.path.join(basedir , 'db.todo')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
#init db
db = SQLAlchemy(app)

class User(db.Model):
	id =db.Column(db.Integer , primary_key=True)
	public_id =db.Column(db.String(200) , unique=True)
	name=db.Column(db.String(200) )
	password =db.Column(db.String(200))
	admin=db.Column(db.Boolean)
class Todo(db.Model):
	id =db.Column(db.Integer , primary_key=True)
	text = db.Column(db.String(200))
	complete=db.Column(db.Boolean)
	user_id = db.Column(db.Integer)
db.create_all()




@app.route('/user' , methods=['GET'])
def get_all_users():
	users = User.query.all()
	output =[]
	for user in users:

		user_data={}
		user_data['public_id'] = user.public_id
		user_data['name'] = user.name
		user_data['password'] = user.password
		user_data['admin'] = user.admin
		output.append(user_data)

	return jsonify({'users' : output})

@app.route('/user/<public_id>' , methods=['GET'])
def get_one_user(public_id):
	user = User.query.filter_by(public_id=public_id).first()
	if not user:
		return jsonify({'message' : 'No User found'})
	user_data={}
	user_data['public_id'] = user.public_id
	user_data['name'] = user.name
	user_data['password'] = user.password
	user_data['admin'] = user.admin
	return jsonify({'user' : user_data})

@app.route('/user' , methods=['post'])
def create_user():
	data=request.get_json()
	hashed_password=generate_password_hash(data['password'] , method='sha256')
	new_user=User(public_id=str(uuid.uuid4()) , name=data['name'] , password=hashed_password , admin=False)
	db.session.add(new_user)
	db.session.commit()
	return jsonify({'message': 'new user created'})

@app.route('/user/<public_id>' , methods=['PUT'])
def promote_users( public_id):
	user = User.query.filter_by(public_id=public_id).first()
	if not user:
		return jsonify({'message' : 'No User found'})
	user.admin=True
	db.session.commit()
	return jsonify({'message':'user has been promoted!'})

@app.route('/user/<public_id>' , methods=['DELETE'])
def delete_user( public_id):
	user = User.query.filter_by(public_id=public_id).first()
	if not user:
		return jsonify({'message' : 'No User found'})
	db.session.delete(user)
	db.session.commit()
	return jsonify({'message':'user has been deleted!!'})
	




if __name__ == '__main__':
	app.run(debug=True)