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
	# print(result)
	return result['name']

def save_material(id, material, qty, delay, updating, app):
	data = {
		"type" : "Materials",
		"material" : material,
		"qty" : qty,
		"delay" : delay
	}
	
	if updating:
		return firebase.put('/Users/' + id, app, data)
	else:
		return firebase.post('/Users/' + id, data)

def save_equipment(id, equipment, qty, updating, app):
	data = {
		"type" : "Equipment",
		"equipment" : equipment,
		"qty" : qty
	}

	if updating:
		return firebase.put('/Users/' + id, app, data)
	else:
		return firebase.post('/Users/' + id, data)

def save_labor(id, qty, quals, updating, app):

	data = {
		"type" : "Labor",
		"qty" : qty,
		"sewing" : quals['sewing'],
		"cooking" : quals['cooking']
	}

	if updating:
		return firebase.put('/Users/' + id, app, data)
	else:
		return firebase.post('/Users/' + id, data)

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
			return redirect(url_for('apply', id=id, app=("new_"+service_type.lower())))
		else:
			flash('Error: All Fields are Required')
			return render_template('dashboard.html', form=form, id=id, biz_data=biz_data)

@app.route('/dashboard/<id>/<app>', methods=['GET','POST'])
def apply(id, app):
	biz_data = find_biz_by_id(id)

	updating = not (app[0:4] == 'new_')
	service = biz_data[app]['type'].lower() if updating else app[4:]

	if request.method == 'GET' :
		if service == "materials":
			if updating:
				form = MaterialsForm(request.form, data=biz_data[app])
				return render_template('apply_materials.html', form=form, id=id, app_id=app, name=biz_data['name'])
			else:
				form = MaterialsForm(request.form) 
				return render_template('apply_materials.html', form=form, id=id, name=biz_data['name'])
		
		if service == "equipment":
			if updating:
				form = EquipmentForm(request.form, data=biz_data[app])
				return render_template('apply_equipment.html', form=form, id=id, app_id=app, name=biz_data['name'])
			else:
				form = EquipmentForm(request.form) 
				return render_template('apply_equipment.html', form=form, id=id, name=biz_data['name'])
		
		if service == "labor":
			if updating:
				form = LaborForm(request.form, data=biz_data[app])
				form.sewing.data = biz_data[app]['sewing']
				form.cooking.data = biz_data[app]['cooking']
				return render_template('apply_labor.html', form=form, id=id, app_id=app, name=biz_data['name'])
			else:
				form = LaborForm(request.form) 
				return render_template('apply_labor.html', form=form, id=id, name=biz_data['name'])

	if request.method == 'POST':

		if service == "materials":
			form = MaterialsForm(request.form)
			material=request.form['material']
			qty=request.form['qty']
			delay=request.form['delay']

			if form.validate():
				save_material(id, material, qty, delay, updating, app)
				return redirect(url_for('dashboard', id=id))
			else:
				flash('Error: All Fields are Required')
				return render_template('apply_materials.html', form=form, id=id, name=biz_data['name'])

		if service == "equipment":
			form = EquipmentForm(request.form)
			equipment=request.form['equipment']
			qty=request.form['qty']

			if form.validate():
				save_equipment(id, equipment, qty, updating, app)
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
				save_labor(id, qty, quals, updating, app)
				return redirect(url_for('dashboard', id=id))
			else:
				flash('Error: All Fields are Required')
				return render_template('apply_labor.html', form=form, id=id, name=biz_data['name'])

if __name__ == "__main__":
	app.run()
