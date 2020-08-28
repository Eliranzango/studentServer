DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS geo_data;
DROP TABLE IF EXISTS student_data;
DROP TABLE IF EXISTS course_data;
CREATE TABLE users (
  id integer primary key autoincrement,
  name string not null,
  email string not null UNIQUE
);
CREATE TABLE geo_data (
  id integer primary key,
  city string not null,
  street string not null,
  street_num integer not null,
  zip_code integer not null,
  latitude NUMERIC(9,6) not null,
  longitude NUMERIC(10,6) not null
);
CREATE TABLE student_data (
  id integer primary key,
  institute string not null,
  major string not null,
  year integer not null
);
CREATE TABLE course_data (
  id integer,
  course string not null
);