from random import randint
from time import strftime
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectField
from firebase import firebase

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'

service_types = [
					("Materials","Materials"),
					("Equipment","Equipment"),
					("Labor","Labor")
				]

class RegisterForm(Form):
	name = TextField('Name:', validators=[validators.required()])
	contact = TextField('Phone #:', validators=[validators.required()])
	loc = TextField("Location:", validators=[validators.required()])
	service_type = SelectField("What you have to offer:", choices=service_types,validators=[validators.required()])

def get_time():
	time = strftime("%Y-%m-%dT%H:%M")
	return time

# def write_to_disk(name, surname, email):
# 	data = open('file.log', 'a')
# 	timestamp = get_time()
# 	data.write('DateStamp={}, Name={}, Surname={}, Email={} \n'.format(timestamp, name, surname, email))
# 	data.close()

firebase = firebase.FirebaseApplication('https://winhacks2020-44957.firebaseio.com', None)
def add_new_biz (name, contact, loc):

	data = {
		"Name" : name,
		"Phone" : contact,
		"Location" : loc
	}

	result = firebase.post('/Users', data);
	print(result)

@app.route("/", methods=['GET','POST'])
def hello():
	form = RegisterForm(request.form)
	return render_template('index.html', form=form)

@app.route("/register", methods=['POST'])
def register():
	form = RegisterForm(request.form)

    #print(form.errors)
	name=request.form['name']
	contact=request.form['contact']
	loc=request.form['loc']
	service_type=request.form['service_type']

	print(service_type)

	# print(name)
	# print(contact)
	# print(loc)

	if form.validate():
		add_new_biz(name, contact, loc)
		flash('Hello: {}'.format(service_type))

	else:
		flash('Error: All Fields are Required')

	return render_template('index.html', form=form)

@app.route('/application/<id>')
def application():
	form = ApplicationForm(request.form)

if __name__ == "__main__":
	app.run()
