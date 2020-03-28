from random import randint
from time import strftime
from flask import *
from firebase import firebase
from forms import *

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'

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

def add_labor(id, quant):

	data = {
		"quant" : quant
	}

	result = firebase.post('/Users/' + id + '/Labor', data)
	# firebase.put('/Users/' + id + '/Labor', "quant", quant)

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

@app.route('/apply/<id>', methods=['GET','POST'])
def apply(id):
	biz_data = find_biz(id)

	if request.method == 'GET' :
		if biz_data['service'] == "Materials":
			return render_template('apply_materials.html', name=biz_data['name'])
		elif biz_data['service'] == "Equipment":
			return render_template('apply_equipment.html', name=biz_data['name'])
		elif biz_data['service'] == "Labor":
			form = LaborForm(request.form)
			return render_template('apply_labor.html', form=form, id=id, name=biz_data['name'])
		else:
			return render_template("error")

	if request.method == 'POST':
		if biz_data['service'] == "Materials":
			return render_template('apply_materials.html', name=biz_data['name'])
		elif biz_data['service'] == "Equipment":
			return render_template('apply_equipment.html', name=biz_data['name'])
		elif biz_data['service'] == "Labor":
			form = LaborForm(request.form)
			quant=request.form['quant']

			if form.validate():
				add_labor(id, quant)
				return quant
			else:
				flash('Error: All Fields are Required')
				return render_template('apply_labor.html', form=form, id=id, name=biz_data['name'])
		else:
			return "error"

if __name__ == "__main__":
	app.run()
