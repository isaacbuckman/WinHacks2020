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
def add_new_biz (name, contact, loc):

	data = {
		"name" : name,
		"phone" : contact,
		"location" : loc
	}

	result = firebase.post('/Users', data);
	print(result)
	return result['name']

def add_material(id, material, qty, delay):
	data = {
		"type" : "Materials",
		"material" : material,
		"qty" : qty,
		"delay" : delay
	}

	result = firebase.post('/Users/' + id, data)

def add_equipment(id, equipment, qty):
	data = {
		"type" : "Equipment",
		"equipment" : equipment,
		"qty" : qty
	}

	result = firebase.post('/Users/' + id, data)

def add_labor(id, qty, quals):

	data = {
		"type" : "Labor",
		"qty" : qty,
		"sewing" : quals['sewing'],
		"cooking" : quals['cooking']
	}

	result = firebase.post('/Users/' + id, data)
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

		if form.validate():
			id = add_new_biz(name, contact, loc)

			return redirect(url_for('dashboard', id=id))

		else:
			flash('Error: All Fields are Required')
			return render_template('register.html', form=form)

@app.route('/dashboard/<id>', methods=['GET', 'POST'])
def dashboard(id):
	biz_data = find_biz_by_id(id)

	if request.method == 'GET' :
		form = DashboardForm(request.form)
		return render_template('dashboard.html', form=form, id=id, biz_data=biz_data)

	if request.method == 'POST' :
		form = DashboardForm(request.form)
		service_type=request.form['service_type']

		if form.validate():
			return redirect(url_for('apply', id=id, service=service_type.lower()))
		else:
			flash('Error: All Fields are Required')
			return render_template('dashboard.html', form=form, id=id, biz_data=biz_data)

@app.route('/dashboard/<id>/new/<any(materials,equipment,labor):service>', methods=['GET','POST'])
def apply(id, service):
	biz_data = find_biz_by_id(id)

	if request.method == 'GET' :
		if service == "materials":
			form = MaterialsForm(request.form)
			return render_template('apply_materials.html', form=form, id=id, name=biz_data['name'])
		
		if service == "equipment":
			form = EquipmentForm(request.form)
			return render_template('apply_equipment.html', form=form, id=id, name=biz_data['name'])
		
		if service == "labor":
			form = LaborForm(request.form)
			return render_template('apply_labor.html', form=form, id=id, name=biz_data['name'])

	if request.method == 'POST':

		if service == "materials":
			form = MaterialsForm(request.form)
			material=request.form['material']
			qty=request.form['qty']
			delay=request.form['delay']

			if form.validate():
				add_material(id, material, qty, delay)
				return redirect(url_for('dashboard', id=id))
			else:
				flash('Error: All Fields are Required')
				return render_template('apply_materials.html', form=form, id=id, name=biz_data['name'])

		if service == "equipment":
			form = EquipmentForm(request.form)
			equipment=request.form['equipment']
			qty=request.form['qty']

			if form.validate():
				add_equipment(id, equipment, qty)
				return redirect(url_for('dashboard', id=id))
			else:
				flash('Error: All Fields are Required')
				return render_template('apply_equipment.html', form=form, id=id, name=biz_data['name'])
		
		if service == "labor":
			form = LaborForm(request.form)
			qty=request.form['qty']
			quals = {}
			quals['sewing'] = form.sewing.data
			quals['cooking'] = form.cooking.data

			if form.validate():
				add_labor(id, qty, quals)
				return redirect(url_for('dashboard', id=id))
			else:
				flash('Error: All Fields are Required')
				return render_template('apply_labor.html', form=form, id=id, name=biz_data['name'])

if __name__ == "__main__":
	app.run()
