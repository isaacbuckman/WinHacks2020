from random import randint
from time import strftime
from flask import *
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

# def get_time():
# 	time = strftime("%Y-%m-%dT%H:%M")
# 	return time

firebase = firebase.FirebaseApplication('https://winhacks2020-44957.firebaseio.com', None)
def add_new_biz (name, contact, loc, service_type):

	data = {
		"Name" : name,
		"Phone" : contact,
		"Location" : loc,
		"Service" : service_type
	}

	result = firebase.post('/Users', data);
	print(result)
	return result['name']

def find_biz(id):
	result = firebase.get('/Users', id)
	return result

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

	if form.validate():
		name = add_new_biz(name, contact, loc, service_type)

		flash('Hello: {}'.format(name))
		# return render_template('index.html', form=form)
		return redirect(url_for('apply', id=name))

	else:
		flash('Error: All Fields are Required')
		return render_template('index.html', form=form)

@app.route('/apply/<id>')
def apply(id):
	return render_template('apply.html', id=find_biz(id))
	# form = ApplyForm(request.form)

if __name__ == "__main__":
	app.run()
