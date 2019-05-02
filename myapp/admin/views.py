from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import Conferenceform, Workshopform
from .. import db
from ..models import Conference, Workshop


@admin.route('/conferences/add', methods=['GET', 'POST'])
#@login_required
def add_conference():
    """
    Add a conference to the database
    """


    add_conference = True

    form = Conferenceform()
    if form.validate_on_submit():

        conference1 = Conference(name=form.name.data, description=form.description.data, startdate=form.startdate.data, enddate=form.enddate.data)
        occupiedDates= Conference.query.all()
        for date in occupiedDates:
            if date.startdate < conference1.startdate and date.enddate >= conference1.startdate:
                conference1.startdate = date.startdate
        try:
            # add department to the database
            db.session.add(conference1)
            db.session.commit()

            flash('You have successfully added a new conference.')
            flash('You have successfully added a new conference.')
        except:
            # in case department name already exists

            flash('Error: sorry that date is occupied.')

        # redirect to departments page
        return redirect(url_for('home.homepage'))
    else:
        flash('Error: did not validate')

    # load department template
    return render_template('admin/conferences/conference.html', action="Add",
                           add_conference=add_conference, form=form,
                           title="Add Conference")
@admin.route('/workshops/add/<confid>',methods=['GET','POST'])
def add_workshop(confid):
    add_workshop=True
    form= Workshopform()
    if form.validate_on_submit():

        workshop1 = Workshop(name=form.name.data, description=form.description.data, starttime=form.starttime.data, endtime=form.endtime.data,conference_id=confid)


        try:
            # add department to the database
            db.session.add(workshop1)
            db.session.commit()

            flash('You have successfully added a new conference.')
        except:
            # in case department name already exists

            flash('Error: sorry that date is occupied.')

        # redirect to departments page
        return redirect(url_for('home.seeconf',confid=confid))
    else:
        flash('Error: did not validate')

    # load department template
    return render_template('admin/workshops/workshop.html', action="Add",
                           add_workshop=add_workshop, form=form,
                           title="Add Workshop")







@admin.route('/testing', methods=['GET', 'POST'])
#@login_required
def testing():
    return 'hello world'
