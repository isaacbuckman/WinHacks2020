from random import randint
from time import strftime
from flask import *
from firebase import firebase
from forms import *

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'



# def get_time():
# 	time = strftime("%Y-%m-%dT%H:%M")
# 	return time

firebase = firebase.FirebaseApplication('https://winhacks2020-44957.firebaseio.com', None)
def add_new_biz (name, contact, loc, service_type):

	data = {
		"name" : name,
		"phone" : contact,
		"location" : loc,
		"service" : service_type
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

		# flash('Hello: {}'.format(name))
		# return render_template('index.html', form=form)
		return redirect(url_for('apply', id=name))

	else:
		flash('Error: All Fields are Required')
		return render_template('index.html', form=form)

@app.route('/apply/<id>')
def apply(id):
	biz_data = find_biz(id)
	if biz_data['service'] == "Materials":
		return render_template('apply_materials.html', name=biz_data['name'])
	elif biz_data['service'] == "Equipment":
		return render_template('apply_equipment.html', name=biz_data['name'])
	elif biz_data['service'] == "Labor":
		form = LaborForm(request.form)
		return render_template('apply_labor.html', form=form, name=biz_data['name'])
	else:
		return render_template("error")

	
	# form = ApplyForm(request.form)

if __name__ == "__main__":
	app.run()
