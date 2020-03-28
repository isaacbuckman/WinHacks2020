from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectField

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

class LaborForm(Form):
	quant = TextField('Number of People:', validators=[validators.required()])

class MaterialsForm(Form):
	yes= True

class EquipmentForm(Form):
	yes = True