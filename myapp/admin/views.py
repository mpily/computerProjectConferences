import datetime
from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy import desc
from . import admin
from .forms import Conferenceform, Workshopform
from .. import db
from ..models import Conference, Workshop,Event,Attend,Room
def deleteShop(shopid):
    shop = Workshop.query.get_or_404(shopid)
    events=Event.query.filter_by(workshop_id=shopid)
    attends = Attend.query.filter_by(Workshhop_id=shopid)
    for event in events:
        db.session.delete(event)
        db.session.commit()
    for attend in attends:
        db.session.delete(attend)
        db.session.commit()
    db.session.delete(shop)
    db.session.commit()

def checkWorkshops(confid,shopid):
    conference1 = Conference.query.get_or_404(confid)
    shop1 = Workshop.query.get_or_404(shopid)
    atime =  shop1.starttime.date()
    btime =  shop1.endtime.date()
    if conference1.startdate > atime or conference1.enddate < btime or btime < atime:
          deleteShop(shop1.id)
@admin.route('/conferences/add', methods=['GET', 'POST'])
@login_required
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
            elif conference1.startdate < date.startdate and  conference1.enddate>=date.startdate :
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



@admin.route('/conferences/edit/<confid>',methods= ['GET','POST'])
@login_required
def edit_conference(confid):
    conference = Conference.query.get_or_404(confid)
    form = Conferenceform(obj=conference)
    if form.validate_on_submit():
        conference.name = form.name.data
        conference.description = form.description.data
        conference.startdate=form.startdate.data
        conference.enddate=form.enddate.data
        db.session.commit()
        shops = Workshop.query.filter_by(conference_id=confid)
        for shop in shops:
            checkWorkshops(confid,shop.id)
        flash('You have successfully edited the conference.')

        # redirect to the departments page
        return redirect(url_for('home.seeconf',confid=confid))

    form.description.data = conference.description
    form.name.data = conference.name
    form.startdate.data =conference.startdate
    form.enddate.data=conference.enddate

    return render_template('admin/conferences/conference.html', action="Edit",
                           add_conference=add_conference, form=form,
                           title="Edit Conference")

@admin.route('/conferences/delete/<int:confid>', methods=['GET', 'POST'])
@login_required
def delete_conference(confid):
    """
    Delete a department from the database
    """
    conference = Conference.query.get_or_404(confid)
    shops = Workshop.query.filter_by(conference_id=confid)
    for shop in shops:
        deleteShop(shop.id)
    db.session.delete(conference)
    db.session.commit()
    flash('You have successfully deleted the conference.')

    # redirect to the departments page
    return redirect(url_for('home.homepage'))

    return render_template(title="Delete Department")

@admin.route('/workshops/add/<confid>',methods=['GET','POST'])
@login_required
def add_workshop(confid):
    add_workshop=True
    form= Workshopform()
    if form.validate_on_submit():
        workshop1 = Workshop(name=form.name.data, description=form.description.data, starttime=form.starttime.data, endtime=form.endtime.data,conference_id=confid)
        '''checking whether it is within the dates of the conference '''
        conference1 = Conference.query.get_or_404(confid)
        atime =  workshop1.starttime.date()
        btime =  workshop1.endtime.date()
        if conference1.startdate > atime or conference1.enddate < btime or btime < atime:
            flash('Error: sorry that date has no conference.')
            return redirect(url_for('home.seeconf',confid=confid))

        else:
            ''' checking whether a room will be available during that time'''
            duringstart = 0
            duringstop = 0
            avrooms = Room.query.count()
            shops = Workshop.query.filter_by(conference_id=confid)
            for shop in shops:
                if workshop1.starttime >= shop.starttime and workshop1.starttime <= shop.endtime:
                    duringstart=duringstart+1
                elif workshop1.endtime >= shop.starttime and workshop1.endtime <=shop.endtime:
                    duringstop=duringstop+1
            if duringstart >= avrooms or duringstop >= avrooms:
                workshop1.id = shops[0].id

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

@admin.route('/workshop/edit/<shopid>',methods= ['GET','POST'])
@login_required
def edit_workshop(shopid):
    workshop= Workshop.query.get_or_404(shopid)
    confid=workshop.conference_id
    form = Workshopform(obj=workshop)
    if form.validate_on_submit():
        workshop.name = form.name.data
        workshop.description = form.description.data
        workshop.starttime=form.starttime.data
        workshop.endtime=form.endtime.data

        db.session.commit()
        flash('You have successfully edited the workshop.')

        # redirect to the departments page
        return redirect(url_for('home.seeconf',confid=confid))

    form.description.data = workshop.description
    form.name.data = workshop.name
    form.starttime.data =workshop.starttime
    form.endtime.data=workshop.endtime


    return render_template('admin/workshops/workshop.html', action="Edit",
                           add_workshop=add_workshop, form=form,
                           title="Edit Conference")

@admin.route('/workshops/delete/<int:shopid>', methods=['GET', 'POST'])
@login_required
def delete_workshop(shopid):
    """
    Delete a department from the database
    """
    shop = Workshop.query.get_or_404(shopid)
    confid = shop.conference_id
    deleteShop(shopid)
    flash('You have successfully deleted the conference.')

    # redirect to the departments page
    return redirect(url_for('home.seeconf',confid=confid))

    return render_template(title="workshop")


def isAvailable(room,shop):
    occupied = Event.query.filter_by(room_number=room.room_number,floor_number=room.floor_number)
    #checking if when the workshop is starting there is another workshop going on
    for othershop in occupied:
        if othershop.starttime <= shop.starttime and othershop.endtime >= shop.starttime:
            return False
    #checking if there is another shop scheduled to start while this one is ongoing
    for other in occupied:
        if shop.starttime <= other.starttime and shop.endtime >=other.endtime:
            return False

    return True

def sortkey(t):
    return t[1]

@admin.route('/conference/endregistration/<int:confid>',methods=['GET','POST'])
@login_required
def endregistration(confid):
    """
    When the time for registration comes to an end this function automatically assigns
    rooms to the workshops and inhibits people from registering
    """
    currconf = Conference.query.get(confid)
    currconf.registrationClosed=True
    db.session.commit()
    temp = Workshop.query.filter_by(conference_id=confid)
    temp1 = []
    for shop in temp:
        temp1.append((shop,Event.query.filter_by(workshop_id=shop.id).count()))
    temp2 = sorted(temp1,reverse=True,key=sortkey)
    toassign =[]
    for i in temp2:
        toassign.append(i[0])
    rooms= Room.query.order_by(desc(Room.capacity))
    for shop in toassign:
        for room in rooms:
            try:
                if isAvailable(room,shop):
                    part=Attend.query.filter_by(Workshhop_id=shop.id).count()
                    event1 = Event(room_number=room.room_number,floor_number=room.floor_number,
                              workshop_id=shop.id,workshopname=shop.name,participants=part,starttime=shop.starttime,endtime=shop.endtime)
                    db.session.add(event1)
                    db.session.commit()
                    break
            except :
                break
    return redirect(url_for('home.seeconf',confid=confid))

@admin.route('/conference/openregistration/<int:confid>',methods=['GET','POST'])
@login_required
def openregistration(confid):
    """
    When the time for registration comes to an end this function automatically assigns
    rooms to the workshops and inhibits people from registering
    """
    currconf = Conference.query.get(confid)
    currconf.registrationClosed=False
    db.session.commit()
    unassign = Workshop.query.filter_by(conference_id=confid)
    rooms = Room.query.all()
    for shop in unassign:
        event=Event.query.filter_by(workshop_id=shop.id)[0]
        db.session.delete(event)
        db.session.commit()


    return redirect(url_for('home.seeconf',confid=confid))


@admin.route('/testing', methods=['GET', 'POST'])
#@login_required
def testing():
    return 'hello world'
