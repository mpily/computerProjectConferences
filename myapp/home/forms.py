from flask_wtf import FlaskForm
from wtforms import   SubmitField 



class RegistrationForm(FlaskForm):
    submit = SubmitField('Register')
