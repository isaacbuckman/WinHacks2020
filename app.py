#use print("", file=sys.stderr) to debug

from random import randint
from time import strftime
from flask import *
from firebase import firebase
from forms import *
import sys

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

def add_material(id, material, qty, delay):
	data = {
		"material" : material,
		"qty" : qty,
		"delay" : delay
	}

	result = firebase.post('/Users/' + id + '/Materials', data)

def add_equipment(id, equipment, qty):
	data = {
		"equipment" : equipment,
		"qty" : qty
	}

	result = firebase.post('/Users/' + id + '/Equipment', data)

def add_labor(id, qty, quals):

	data = {
		"qty" : qty,
		"sewing" : quals['sewing'],
		"cooking" : quals['cooking']
	}

	result = firebase.post('/Users/' + id + '/Labor', data)
	# firebase.put('/Users/' + id + '/Labor', "qty", qty)

def find_biz_by_id(id):
	result = firebase.get('/Users', id)
	return result

#TODO: Optimize using a lookup table
def find_id_by_name(name):
	users = firebase.get('/Users', None)
	for user_id in users:
		if name == firebase.get('/Users', user_id)['name']:
			return user_id
	return False

@app.route("/", methods=['GET','POST'])
def login():
	if  request.method == 'GET':
		form = LoginForm(request.form)
		return render_template('index.html', form=form)

	if request.method == 'POST':
		form = LoginForm(request.form)
		name=request.form['name']

		if form.validate():
			id = find_id_by_name(name)
			if id:
				return redirect(url_for('dashboard', id=id))
			else:
				flash('Error: You are not registered')
				return render_template('index.html', form=form)
		else:
			flash('Error: All Fields are Required')
			return render_template('index.html', form=form)

@app.route("/register", methods=['GET','POST'])
def register():
	if request.method == 'GET':
		form = RegisterForm(request.form)
		return render_template('register.html', form=form)

	if request.method == 'POST':
		form = RegisterForm(request.form)
		name=request.form['name']
		contact=request.form['contact']
		loc=request.form['loc']
		service_type=request.form['service_type']

		if form.validate():
			id = add_new_biz(name, contact, loc, service_type)

			# flash('Hello: {}'.format(name))
			# return render_template('index.html', form=form)
			return redirect(url_for('apply', id=id))

		else:
			flash('Error: All Fields are Required')
			return render_template('register.html', form=form)

@app.route('/dashboard/<id>', methods=['GET'])
def dashboard(id):
	biz_data = find_biz_by_id(id)

	if request.method == 'GET' :
		# return render_template('dashboard.html', biz_data=biz_data)
		return str(biz_data)

@app.route('/apply/<id>', methods=['GET','POST'])
def apply(id):
	biz_data = find_biz_by_id(id)

	if request.method == 'GET' :
		
		if biz_data['service'] == "Materials":
			form = MaterialsForm(request.form)
			return render_template('apply_materials.html', form=form, id=id, name=biz_data['name'])
		
		if biz_data['service'] == "Equipment":
			form = EquipmentForm(request.form)
			return render_template('apply_equipment.html', form=form, id=id, name=biz_data['name'])
		
		if biz_data['service'] == "Labor":
			form = LaborForm(request.form)
			return render_template('apply_labor.html', form=form, id=id, name=biz_data['name'])

	if request.method == 'POST':

		if biz_data['service'] == "Materials":
			form = MaterialsForm(request.form)
			material=request.form['material']
			qty=request.form['qty']
			delay=request.form['delay']

			if form.validate():
				add_material(id, material, qty, delay)
				return "" + material + " " + qty + " " + delay
			else:
				flash('Error: All Fields are Required')
				return render_template('apply_materials.html', form=form, id=id, name=biz_data['name'])

		if biz_data['service'] == "Equipment":
			form = EquipmentForm(request.form)
			equipment=request.form['equipment']
			qty=request.form['qty']

			if form.validate():
				add_equipment(id, equipment, qty)
				return "" + equipment + " " + qty
			else:
				flash('Error: All Fields are Required')
				return render_template('apply_equipment.html', form=form, id=id, name=biz_data['name'])
		
		if biz_data['service'] == "Labor":
			form = LaborForm(request.form)
			qty=request.form['qty']
			quals = {}
			quals['sewing'] = form.sewing.data
			quals['cooking'] = form.cooking.data

			if form.validate():
				add_labor(id, qty, quals)
				return str(quals)
			else:
				flash('Error: All Fields are Required')
				return render_template('apply_labor.html', form=form, id=id, name=biz_data['name'])

if __name__ == "__main__":
	app.run()
