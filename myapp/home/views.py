import re , datetime, calendar

from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from sqlalchemy import desc
from wtforms.validators import DataRequired
from  ..models import Conference, Workshop,Participant,Attend, Event,Room
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

    elif adjustment == 'pyear':
      month = int(request.form.get('prevmonth'))
      year = int(request.form.get('prevyear'))
      year = year -1

    if adjustment == 'pmonth' :
      month = (int(request.form.get('prevmonth'))-1)
      year = int(request.form.get('prevyear'))
      if month == 0:
          month = 12
          year = year-1


  for i in range (1,32):
       temp = Day(i,month,year)
       for date in occupiedDates:
          if date.startdate <= temp.mydate and date.enddate >= temp.mydate:
              temp.event = date.id
       theMonth.append(temp)

  monthrep = Monthify(theMonth)
  return render_template('home/home.html',month=monthrep,year= str(year),monthname= str(month),conferences=Conference.query.all())

@home.route('/Conference/<confid>/',methods=['GET','POST'])
@login_required
def seeconf(confid):

    currconf=Conference.query.filter_by(id=int(confid))
    myworkshops=Workshop.query.filter_by(conference_id=int(confid))
    events= []
    if currconf[0].registrationClosed:
        for workshop in myworkshops:
             events.append(Event.query.filter_by(workshop_id=workshop.id)[0])

    return render_template('home/conf.html',conf=currconf ,workshops=myworkshops,events=events )

@home.route('/Workshop/<shopid>/',methods=['GET','POST'])
@login_required
def seeshop(shopid):
    currshop=Workshop.query.filter_by(id=shopid)
    ashop = currshop[0]
    rooms= Room.query.order_by(desc(Room.capacity))
    form = RegistrationForm()
    roomNumber = 0
    shops= Workshop.query.filter_by(conference_id=currshop[0].conference_id)
    for shop in shops:
        if shop.id == ashop.id:
            continue
        elif shop.starttime <= ashop.starttime and shop.endtime >= ashop.starttime and Attend.query.filter_by(Workshhop_id=shop.id).count() > Attend.query.filter_by(Workshhop_id=ashop.id).count():
            roomNumber = roomNumber+1
        elif ashop.starttime <= shop.starttime and ashop.endtime >= shop.starttime and Attend.query.filter_by(Workshhop_id=shop.id).count() > Attend.query.filter_by(Workshhop_id=ashop.id).count():
            roomNumber = roomNumber+1
    if request.method== 'POST':
     action = request.form.get('foo')
     if action == 'register':
        attend1 = Attend(email=current_user.email,
                           Workshhop_id=shopid)
        try:
            db.session.add(attend1)
            db.session.commit()
            flash('you have successfully signedup for the workshop')
        except:
            flash('you already signedup for the workshop')
            return redirect(url_for('home.homepage'))

     elif action == 'deregister':
        try:
            prevattend = Attend.query.filter_by(Workshhop_id=shopid,email=current_user.email)[0]
            db.session.delete(prevattend)
            db.session.commit()
            flash("you have successfully deregistered for the conference")
        except:
            flash("you weren't registered in the first place")
            return redirect(url_for('home.homepage'))


        # redirect to the login page
        return redirect(url_for('home.seeconf',confid=currshop[0].conference_id))


    return render_template('home/shop.html',shops=currshop,totattend= Attend.query.filter_by(Workshhop_id=shopid),form=form, maxpop=rooms[roomNumber].capacity)
