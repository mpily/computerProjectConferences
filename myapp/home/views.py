import re , datetime, calendar

from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired
from  ..models import Conference, Workshop,Participant,Attend
from .. import db
from . import home
from .forms import RegistrationForm

class Day(object):
    """docstring for Day."""
    def __init__(self, day, month,year):
        daymap = {"Sunday" : 0,"Monday" : 1, "Tuesday" : 2, "Wednesday" : 3, "Thursday":4, "Friday":5, "Saturday":6 }
        try:
          self.mydate = datetime.date(year,month,day)
          temp =  self.mydate.strftime('%A')
          self.date = day
          self.weekday = daymap[temp]
          self.event = 0
        except:
            self.mydate = datetime.date(1980,1,1)
            self.date = 1000
            self.weekday = daymap["Friday"]
            self.event =0
    def __repr__(self):
        if self.date == 1000:
            return ""
        return str(self.date)

def Monthify(days):

    monthrep = []

    for day in days:
        if day.date == 1:
            temp = []
            monthrep.append(temp)
            for i in range(day.weekday):
                monthrep[0].append('')
        monthrep[-1].append(day)
        if day.weekday == 6:
            temp = []
            monthrep.append(temp)

    return monthrep

@home.route('/',methods=['GET','POST'])
def homepage():
  occupiedDates = Conference.query.all()
  temp = datetime.date.today()
  month = temp.month
  year = temp.year

  theMonth = []
  if request.method == 'POST':
    adjustment = request.form.get('foo')  # access the data inside

    if adjustment == 'month' :
      month = (int(request.form.get('prevmonth'))+1)%13
      year = int(request.form.get('prevyear'))
      if month == 0:
          month = 1
          year = year+1

    elif adjustment == 'year':
      month = int(request.form.get('prevmonth'))
      year = int(request.form.get('prevyear'))
      year = year +1

  for i in range (1,32):
       temp = Day(i,month,year)
       for date in occupiedDates:
          if date.startdate <= temp.mydate and date.enddate >= temp.mydate:
              temp.event = date.id
       theMonth.append(temp)

  monthrep = Monthify(theMonth)
  return render_template('home/home.html',month=monthrep,year= str(year),monthname= str(month))

@home.route('/Conference/<confid>/',methods=['GET','POST'])
def seeconf(confid):
    currconf=Conference.query.filter_by(id=confid)
    myworkshops=Workshop.query.filter_by(conference_id=confid)
    return render_template('home/conf.html',conf=currconf ,workshops=myworkshops)

@home.route('/Workshop/<shopid>/',methods=['GET','POST'])
@login_required
def seeshop(shopid):
    currshop=Workshop.query.filter_by(id=shopid)
    form = RegistrationForm()
    if form.validate_on_submit():
        attend1 = Attend(email=current_user.email,
                          Workshhop_id=shopid)

        # add employee to the database
        db.session.add(attend1)
        db.session.commit()
        flash('you have successfully signedup for the workshop')

        # redirect to the login page
        return redirect(url_for('home.seeconf',confid=currshop[0].conference_id))


    return render_template('home/shop.html',shops=currshop,totattend= Attend.query.filter_by(Workshhop_id=shopid),form=form)
