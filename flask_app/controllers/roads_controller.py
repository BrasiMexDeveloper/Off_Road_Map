from flask_app import app
from flask import render_template, redirect, request, session,flash
from flask_app.models.roads_model import Roads


#?=========create page=============


@app.route('/utv/new')
def new_roads_utv():
    return render_template("utv_roads.html")
    


#?=========create action post=============

@app.route('/utv/create', methods=['POST'])
def roads_utv():
    print(f'==========={request.form}=======')
    if not Roads.validator(request.form):
        return redirect("/utv/new")

    roads_data = {
        **request.form,
        'user_id': session['user_id']

    }
    Roads.roads_utv(roads_data)
    return redirect("/road/view")


#?=======read all view ==========

@app.route('/road/view')
def display_all():
    all_roads = Roads.get_all()
    return render_template("view_roads.html",all_roads=all_roads)

#?=======read one view ==========

@app.route('/road/<int:id>/view')
def display_roads(id):
    this_roads = Roads.get_by_id({'id': id})
    return render_template("planing_ride.html",this_roads=this_roads)

#?=======delete one========

@app.route('/road/<int:id>/clear')
def  delete_shows(id):
    Roads.delete({'id':id})
    return redirect("/road/view")
    