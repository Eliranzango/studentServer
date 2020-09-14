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
    #res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers.add("Access-Control-Allow-Origin", "http://83.130.145.225:8080")
    res.headers.add('Access-Control-Allow-Credentials', 'true')
    #res.headers['Access-Control-Allow-Credentials'] = 'True'
    res.set_cookie('userID', json.dumps(id),secure=False,samesite=None)
    return res

@app.route('/user-marker',methods=['GET'])
def user_marker():
    userID = request.cookies.get('userID')
    if (userID == None):
        d = "ERROR: didnt get user ID in cookie"
        print(d)
        response = d, 404
        res = app.make_response(response)
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Credentials'] = 'True'
        return res
    print(userID)
    id = int(userID)
    u = User.query.filter(User.id == id).first()
    c = geoData.query.filter(geoData.id == id).first()
    userData = {'name': u.name, 'email': u.email,'phone': u.phone ,'location': {'lat': float(c.latitude), 'lng': float(c.longitude)}}
    print(userData)
    response = jsonify(userData), 200
    res = app.make_response(response)
    res.headers.add("Access-Control-Allow-Origin", "*")
    res.headers.add('Access-Control-Allow-Credentials', 'true')
    return res

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
def add_user_data():
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
    coords = data["location"]
    lat = coords["lat"]
    lng = coords["lng"]
    institute = data["institute"]
    major= data["major"]
    year = data["year"]
    courses = data["courses"]
    zipCode = 0
    user = User(name, email,phone)
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
        geo = geoData(id,city,country,street,streetNum,zipCode,lat,lng)
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

@app.route('/update-user-info',methods=['POST','GET'])
def update_user_data():
    userID = request.cookies.get('userID')
    #userID = 3
    if (userID == None):
        d = "ERROR: didnt get user ID in cookie"
        print(d)
        response = d, 404
        res = app.make_response(response)
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Credentials'] = 'True'
        return res
    selectedUser = User.query.filter(User.id == userID).first()
    selectedGeoData = geoData.query.filter(geoData.id == userID).first()
    selectedStuData = studentData.query.filter(studentData.id == userID).first()
    courseData.query.filter(courseData.userID == userID).delete()
    data = request.get_data()
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    s = json.dumps(data, indent=4, sort_keys=True)
    print(s)
    selectedUser.name = data["name"]
    selectedUser.email = data["email"]
    selectedUser.phone = data["phone"]
    selectedGeoData.street = data["street"]
    selectedGeoData.street_num = data["streetNum"]
    selectedGeoData.city = data["city"]
    selectedGeoData.country = data["country"]
    coords = data["location"]
    selectedGeoData.latitude = coords["lat"]
    selectedGeoData.longitude = coords["lng"]
    selectedStuData.institute = data["institute"]
    selectedStuData.major= data["major"]
    selectedStuData.year = data["year"]
    courses = data["courses"]
    for c in courses:
        cour = courseData(userID, c)
        db.session.add(cour)
    try:
        db.session.commit()
        statusData = "success"
        print("User successfully updated: ", userID)
        status = 200
        print(userID)
    except:
        statusData = "fail"
        print("User failed to be updated")
        userID = 0
        status = 404

    response = jsonify(status=statusData), status
    res = app.make_response(response)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Credentials'] = 'True'
    return res

@app.route('/users-marker',methods=['GET'])
def markers():
    users = db.session.query(User).all() # or you could have used User.query.all()
    data = []
    try:
        for user in users:
            loc = geoData.query.filter(geoData.id == user.id).first()
            data.append({'name':user.name,'email':user.email,'id':user.id, 'phone':user.phone, 'location': {'lat': float(loc.latitude), 'lng': float(loc.longitude)}})
        d = json.dumps(data)
        print(d)
        status = 200
    except:
        status = 404
    response = jsonify(data),status
    res = app.make_response(response)
    res.headers.add("Access-Control-Allow-Origin", "*")
    res.headers.add("Access-Control-Allow-Credentials", "TRUE")
    return res

@app.route('/send-filter',methods=['POST'])
def send_filter():
    data = request.get_data()
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    s = json.dumps(data, indent=4, sort_keys=True)
    print(s)
    inst = data["institute"]
    maj = data["major"]
    year = data["year"]
    courseNum = data["course"]
    selectedIds = []
    stu = studentData.query.filter((studentData.institute==inst)&(studentData.major==maj)&(studentData.year==year)).all()
    courses = courseData.query.filter(courseData.course == courseNum).all()
    for s in stu:
        selectedIds.append(s.id)
    for c in courses:
        selectedIds.append(c.userID)
    selectedIds = set(selectedIds) #remove multiple ids
    filterdData = []
    for id in selectedIds:
        u = User.query.filter(User.id == id).first()
        c = geoData.query.filter(geoData.id == id).first()
        userData = {'name': u.name, 'email': u.email,'coords': {'lat': str(c.latitude), 'lng': str(c.longitude)}}
        filterdData.append(userData)
    status = 200
    d = jsonify(filterdData)
    print (d)
    response = d, status
    res = app.make_response(response)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Credentials'] = 'True'
    return res

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


@app.route('/get-user-info')
def user_info():
    userID = request.cookies.get('userID')
    if (userID == None):
        d = "ERROR: didnt get user ID in cookie"
        print(d)
        response = d, 404
        res = app.make_response(response)
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Credentials'] = 'True'
        return res
    print(userID)
    id = int(userID)
    u = User.query.filter(User.id == id).first()
    g = geoData.query.filter(geoData.id == id).first()
    s = studentData.query.filter(studentData.id == id).first()
    cur = courseData.query.filter(courseData.userID == id).all()
    course = []
    for c in cur:
        course.append(c.course)
    data = {'name': u.name, 'email': u.email,'phone': u.phone ,'street':g.street,'streetNum':g.street_num,'city':g.city,'country':g.country,'location': {'lat': float(g.latitude), 'lng': float(g.longitude)},'institute':s.institute,'major':s.major,'year':s.year,'courses':course}
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
        status = 404

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
