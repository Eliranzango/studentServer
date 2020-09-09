"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for, flash, make_response, jsonify
from app.forms import *
from app.models import *
import json


# import sqlite3

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/login',methods=['POST'])
def login():
    data = request.get_data()
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    s = json.dumps(data, indent=4, sort_keys=True)
    print(s)
    email = data["email"]
    try:
        user = User.query.filter_by(email=email).first()
        status = 200
        statusData = "success"
        id = user.id
    except:
        status = 404
        statusData = "fail"
        id = 0
    response = jsonify(status=statusData), status
    res = app.make_response(response)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Credentials'] = 'True'
    res.set_cookie('userID', json.dumps(id))
    return res

@app.route('/user-marker',methods=['GET'])
def user_marker():
    userID = request.cookies.get('userID')
    print (userID)

@app.route('/test',methods=['POST','GET'])
def test():
    data = request.data
    print("test")
    print (data)
    response = jsonify(test="im alive!")
    res= app.make_response(response)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Credentials'] = 'True'
    res.set_cookie('userID', '12345')
    return res

@app.route('/add-user',methods=['POST','GET'])
def full_data():
    data = request.get_data()
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    s = json.dumps(data, indent=4, sort_keys=True)
    print(s)
    name = data["name"]
    email = data["email"]
    phone = data["phone"]
    street = data["street"]
    streetNum = data["streetNum"]
    city = data["city"]
    country = data["country"]
    coords = data["coords"]
    lat = coords["lat"]
    lng = coords["lng"]
    institute = data["institute"]
    major= data["major"]
    year = data["year"]
    courses = data["courses"]
    zipCode = 0
    user = User(name, email)
    db.session.add(user)
    try:
        db.session.commit()
        statusData = "success"
        flash('User successfully added')
        id = user.id
        print("User successfully added: ", id)
        status = 200
        print(id)
    except:
        statusData = "fail"
        flash('User did not added')
        print("User failed to be added")
        id = 0
        status = 404

    if(status ==200):
        student = studentData(id,institute,major,year)
        db.session.add(student)
        try:
            db.session.commit()
        except:
            print("error adding student to DB")
        geo = geoData(id,city,street,streetNum,zipCode,lat,lng)
        db.session.add(geo)
        try:
            db.session.commit()
        except:
            print("error adding geo to DB")
        for c in courses:
            cour = courseData(id,c)
            db.session.add(cour)
        try:
            db.session.commit()
        except:
            print ("error adding course data to DB")
    response = jsonify(status=statusData), status
    res = app.make_response(response)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Credentials'] = 'True'
    res.set_cookie('userID', json.dumps(id))
    return res

@app.route('/markers',methods=['GET'])
def markers():
    d1 = {'name': 'eliran', 'email': 'Datacamp','phone':'2323','location':{'lat':32.0170737,'lng':34.7681623}}
    d2 = {'name': 'Eden', 'email': 'blalba', 'phone': '2323', 'location': {'lat': 32.0154278, 'lng': 34.7705851}}
    data =[d1,d2]
    response = jsonify(data)
    return response,200

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/user-table')
def show_users():
    users = db.session.query(User).all() # or you could have used User.query.all()
    data = []
    for user in users:
        data.append({'name':user.name,'email':user.email,'id':user.id})
    d = json.dumps(data)
    print(d)
    response = d, 200
    res = app.make_response(response)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Credentials'] = 'True'
    return res

@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    user_form = UserForm()
    if request.method == 'POST':
        data = request.get_data()
        my_json = data.decode('utf8').replace("'", '"')
        print(my_json)
        data = json.loads(my_json)
        s = json.dumps(data, indent=4, sort_keys=True)
        print(s)
        name = data["name"]
        email = data["email"]
        #password = data["password"]
        user = User(name, email)
        db.session.add(user)
        try:
            db.session.commit()
            statusData = "success"
            flash('User successfully added')
            id = user.id
            print ("User successfully added: ",id)
            status = 200
            print(id)
        except:
            statusData = "fail"
            flash('User did not added')
            print("User failed to be added")
            id = 0
            status = 500
        response = jsonify(status=statusData),status
        res= app.make_response(response)
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Credentials'] = 'True'
        res.set_cookie('userID', json.dumps(id))
        return res
        """""
        if user_form.validate_on_submit():
            # Get validated data from form
            name = user_form.name.data # You could also have used request.form['name']
            email = user_form.email.data # You could also have used request.form['email']

            # save user to database
            user = User(name, email)
            db.session.add(user)
            db.session.commit()

            flash('User successfully added')
            return redirect(url_for('show_users'))
        """
    flash_errors(user_form)
    return render_template('add_user.html', form=user_form)

@app.route('/delete-user', methods=['POST', 'GET'])
def delete_user():
    data = request.get_data()
    my_json = data.decode('utf8').replace("'", '"')
    print(my_json)
    data = json.loads(my_json)
    s = json.dumps(data, indent=4, sort_keys=True)
    print(s)
    deletId = data["id"]
    User.query.filter(User.id == deletId).delete()
    studentData.query.filter(studentData.id == deletId).delete()
    geoData.query.filter(geoData.id == deletId).delete()
    courseData.query.filter(courseData.userID == deletId).delete()
    try:
        db.session.commit()
        statusData = "success"
        status = 200
    except:
        statusData = "fail"
        status = 500

    return show_users()


# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
