from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class AddMedicalHistoryForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    visit_type = StringField('Visit Type', [validators.Length(min=4, max=30)])
    report = TextAreaField('Report', [validators.length(min=10, max=200)])
    medicine = TextAreaField('Medicine', [validators.Length(min=4, max=200)])

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators = [DataRequired()])
	submit = SubmitField('Sign In')