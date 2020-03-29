from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectField, BooleanField

service_types = [
					("Materials","Materials"),
					("Equipment","Equipment"),
					("Labor","Labor")
				]

class LoginForm(Form):
	name = TextField('Name:', validators=[validators.required()])
	password = TextField('password:', validators=[validators.required()])

class RegisterForm(Form):
	name = TextField('Company name:', validators=[validators.required()])
	contact_name = TextField('Contact name:', validators=[validators.required()])
	phone = TextField("Phone number:", validators=[validators.required()])
	email = TextField("E-mail:", validators=[validators.required()])
	loc = TextField("Address::", validators=[validators.required()])
	visit = BooleanField("A government official can visit the location.")

class DashboardForm(Form):
	service_type = SelectField("What you have to offer:", choices=service_types)
	prefill = TextField('Prefill Data:')

class MaterialsForm(Form):
	material = TextField('Material Name:', validators=[validators.required()])
	qty = TextField('Quantity:', validators=[validators.required()])
	delay = TextField('Time Delay:', validators=[validators.required()])

class EquipmentForm(Form):
	equipment = TextField('Equipment Type:', validators=[validators.required()])
	qty = TextField('Quantity:', validators=[validators.required()])

class LaborForm(Form):
	qty = TextField('Number of People:', validators=[validators.required()])
	security= BooleanField("Guard/security services") 
	nursing= BooleanField("Nursing services")
	food= BooleanField("Food services")
	laundry= BooleanField("Laundry services")
	accommodation= BooleanField("Accommodation maintenance services")
	personal= BooleanField("Personal services") 
	IT = BooleanField("IT Support services")
