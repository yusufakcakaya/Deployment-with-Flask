from flask import Flask, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import app
import os
import socket


app = Flask(__name__)

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

# Settings for migrations
migrate = Migrate(app, db)

# Models
class Game(db.Model):
	# Id : Field which stores unique id for every row in database table.
	
	id = db.Column(db.Integer, primary_key=True)
	game_name = db.Column(db.String(0))
	required_age = db.Column(db.Integer)
	price = db.Column(db.Integer)

	# repr method represents how one object of this datatable
	# will look like
	def __repr__(self):
		return f"Name : {self.game_name}, Age: {self.required_age}"
        
@app.before_first_request
def create_tables():
    db.create_all()

# function to render index page
@app.route('/')
def index():
	games = Game.query.all()
	return render_template('index.html', games=games)

@app.route('/add_game')
def add_game():
	return render_template('add_game.html')

# function to add profiles
@app.route('/add', methods=["POST"])
def game():
	# In this function we will input data from the
	# form page and store it in our database. 
	game_name = request.form.get("game_name")
	required_age = request.form.get("required_age")
	price = request.form.get("price")

	# create an object of the Profile class of models and
	# store data as a row in our datatable
	if game_name != '' and required_age != '' and price is not None:
		g = Game(game_name=game_name, required_age=required_age, price=price)
		db.session.add(g)
		db.session.commit()
	return redirect('/')

@app.route('/delete/<int:id>')
def erase(id):
	
	# letes the data on the basis of unique id and
	# directs to home page
	data = Game.query.get(id)
	db.session.delete(data)
	db.session.commit()
	return redirect('/')



if __name__ == '__main__':
	hostname = socket.gethostname()
	local_ip = socket.gethostbyname(hostname)
	app.run(host=local_ip, port=os.environ.get('PORT'), debug=True)






   # local_ip = socket.gethostbyname(hostname)
    #app.run(host=local_ip, port=os.environ.get('PORT'), debug=True)
