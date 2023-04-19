from flask_app import app
from flask import render_template, redirect, request, session,flash
from flask_app.models.user_model import User
from flask_app.models.roads_model import Roads


from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
        
    return render_template('registration.html')

#?========CREATE USER=====

@app.route('/create_user')
def create_user():
    return render_template('registration.html')
   


#?========REGISTER=====
@app.route('/register', methods=['POST'])
def reg_user():
    print(request.form)
    if not User.validator(request.form):
        return render_template("registration.html")
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        ** request.form,
        'password': hashed_pw
    }
    user_id = User.create_one(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

#?==========DISPLAY OR DASHBOARD
@app.route('/dashboard')
def login():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    logged_user = User.get_id(data)
    all_roads = Roads.get_all()
    return render_template('dashboard.html',logged_user = logged_user,all_roads = all_roads)

#?=========LOGOUT========
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

#?=========LOGIN=======

@app.route('/login', methods=['POST'])
def login_user():
    data = {'email' : request.form['email']}
    may_a_user = User.get_email(data)
    if not may_a_user:
        flash("invalid credentials")
        return redirect('/')
    if not bcrypt.check_password_hash(may_a_user.password, request.form['password']):
        flash("invalid credentials")
        return redirect('/')
        
    session['user_id'] = may_a_user.id
    return redirect('/dashboard')

    


