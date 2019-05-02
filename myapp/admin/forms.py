from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField,DateTimeField
from wtforms.validators import DataRequired

class Conferenceform(FlaskForm):
    """
    Form for admin to add or edit a conference
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    startdate = DateField('StartDate', validators=[DataRequired()])
    enddate = DateField('EndDate', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Workshopform(FlaskForm):
     """ form for admin to add a workshop."""
     name = StringField('Name',validators=[DataRequired()])
     description = StringField('Description',validators=[DataRequired()])
     starttime =  DateTimeField('starttime',validators=[DataRequired()])
     endtime = DateTimeField('endtime',validators=[DataRequired()])
     submit = SubmitField('Submit')
