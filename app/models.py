from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.name

class studentData(db.Model):
    __tablename__ = 'student_data'
    id = db.Column(db.Integer, primary_key = True)
    institute = db.Column(db.String(255))
    major = db.Column(db.String(255))
    year = db.Column(db.Integer(255))

    def __init__(self, institute, major,year):
        self.institute = institute
        self.major = major
        self.year = year

    def __repr__(self):
        return '<studentDataID %r>' % self.id

class geoData(db.Model):
    __tablename__ = 'geo_data'
    id = db.Column(db.Integer, primary_key = True)
    city = db.Column(db.String(255))
    street = db.Column(db.String(255))
    street_num = db.Column(db.Integer)
    zip_code = db.Column(db.Integer,unique=True)
    latitude = db.Column(db.NUMERIC(9,6))
    longitude = db.Column(db.NUMERIC(10,6))

    def __init__(self, city, street,street_num,zip_code,latitude,longitude):
        self.city = city
        self.street = street
        self.street_num = street_num
        self.zip_code = zip_code
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '<geoDataZip %r>' % self.zip_code

class courseData(db.Model):
    __tablename__ = 'course_data'
    id = db.Column(db.Integer)
    course = db.Column(db.String(255))

    def __init__(self, id,course):
        self.id = id
        self.course = course

    def __repr__(self):
        return '<courseData %r>' % self.course