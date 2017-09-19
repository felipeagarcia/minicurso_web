from flask import Flask
import mongoengine as me
import json
from flask import jsonify


class User(me.Document):
	name = me.StringField()
	email = me.StringField()

class Task (me.Document):
	description = me.StringField()
	deadline = me.DateTimeField()
	title = me.StringField()
	finished = me.BooleanField()
	tags = me.ListField(me.StringField())
	addded = me.DateTimeField()
	user = me.ReferenceField(User)
	color = me.StringField()

app = Flask(__name__)
me.connect("todo_app")
@app.route("/users", methods = ['GET'])
def get_users():
	users = User.objects.all()
	array = []
	for user in users:
		array.append({
			'id':str(user.id),
			'name': user.name,
			'email': user.email
			})
	return jsonify(array)

#def test():
#	return "<div style='background-color: black;'><center><h1 style = 'color: yellow;'> Ola </h1></center></div>"


if __name__ == "__main__":
	app.run()