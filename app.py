from flask import Flask
import mongoengine as me
import json
from flask import jsonify
from flask import request
from datetime import datetime

class User(me.Document):
	name = me.StringField()
	email = me.StringField()
	def to_dict(self):
		return {
				'id':str(self.id),
				'name': self.name,
				'email': self.email
				}


class Task (me.Document):
	description = me.StringField()
	deadline = me.DateTimeField()
	title = me.StringField()
	finished = me.BooleanField()
	tags = me.ListField(me.StringField())
	added = me.DateTimeField()
	user = me.ReferenceField(User)
	color = me.StringField()


	def to_dict(self):
		return{
			'id' : str(self.id),
			'title' : self.title,
			'description' : self.description,
			'finished' : self.finished,
			'tags' : self.tags,
			'added' : int(self.added.timestamp()),
			'user' : str(self.user),
			'color' : self.color,
			'deadline' : int(self.deadline.timestamp()),
				}

app = Flask(__name__)
me.connect("todo_app")
@app.route("/users", methods = ['GET'])
def get_users():
	users = User.objects.all()
	array = []
	for user in users:
		array.append(user.to_dict())
	return jsonify(array)

@app.route("/users", methods = ['POST'])
def create_user():
	if not request.is_json:
		return jsonify({'error':'not_json'}), 400
	data = request.get_json()
	name = data.get('name')
	email = data.get('email')
	user = User (name = name, email = email)
	user.save()
	return jsonify(user.to_dict())

@app.route("/tasks", methods = ['GET'])
def get_tasks():
	tasks = Task.objects.all()
	array = []
	for task in tasks:
		array.append(task.to_dict())
	return jsonify(array)

@app.route("/tasks", methods = ['POST'])
def create_task():
	if not request.is_json:
		return jsonify({'error':'not_json'}), 400
	data = request.get_json()
	title = data.get('title')
	description = data.get('description')
	finished = False
	tags = data.get('tags', [])
	added = datetime.now()
	user = data.get('user')
	color = data.get('color')
	deadline = datetime.fromtimestamp(data.get('deadline', 0))
	if 'user' in data:
		user = User.objects.filter(id = data.get('user')).first()
	task = Task (description = description, deadline = deadline, title = title,
				 finished = finished, tags = tags, added = added, user = user, color = color)
	task.save()
	return jsonify(task.to_dict())

@app.route("/tasks/<string:task_id>", methods = [PATCH])
def att_tasks(task_id):
	if not request.is_json:
		return jsonify({'error':'not_json'}), 400
	data = request.get_json()
	task = Task.objects.filter(id =data.get('id'))
	if not task:
		return jsonify({'error':'not_found'}), 400

	task.complete = data.get('complete', task.complete)
	task.save()
	return jsonify(task.to_dict())

if __name__ == "__main__":
	app.run(debug = True)