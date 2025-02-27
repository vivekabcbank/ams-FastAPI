from .database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class UserType(Base):
    __tablename__ = 'usertype'

    id = Column(Integer, primary_key=True)
    typename = Column(String(200), nullable=True)
    description = Column(String, nullable=True)
    isdeleted = Column(Boolean, default=False)
    createddate = Column(DateTime, default=datetime.utcnow, nullable=False)
    updateddate = Column(DateTime, nullable=True)

    def __str__(self):
        return f"{self.typename}"


class Country(Base):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True)
    countryname = Column(String(200), default="")
    sortname = Column(String(200), default="")
    countrycode = Column(String(200), default="")
    isdeleted = Column(Boolean, default=False)
    createddate = Column(DateTime, default=datetime.utcnow, nullable=False)
    updateddate = Column(DateTime, nullable=True)

    def __str__(self):
        return f"{self.countryname}"


class State(Base):
    __tablename__ = 'state'

    id = Column(Integer, primary_key=True)
    countryid = Column(Integer, ForeignKey('country.id'), nullable=True)
    statename = Column(String(200))
    isdeleted = Column(Boolean, default=False)
    createddate = Column(DateTime, default=datetime.utcnow, nullable=False)
    updateddate = Column(DateTime, nullable=True)

    # Relationship with Country
    country = relationship('Country', backref='states')

    def __str__(self):
        return f"{self.statename}"


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    stateid = Column(Integer, ForeignKey('state.id'), nullable=True)
    cityname = Column(String(200))
    isdeleted = Column(Boolean, default=False)
    createddate = Column(DateTime, default=datetime.utcnow, nullable=False)
    updateddate = Column(DateTime, nullable=True)

    # Relationship with State
    state = relationship('State', backref='cities')

    def __str__(self):
        return f"{self.cityname}"


class User(Base):
    __tablename__ = 'auth_user'

    id = Column(Integer, primary_key=True)
    company_name = Column(String(250))
    first_name = Column(String(250))
    last_name = Column(String(250))
    username = Column(String(120), unique=True, nullable=True)
    email = Column(String(120), nullable=True)
    password = Column(String(128), nullable=True)
    usertype_id = Column(Integer, ForeignKey('usertype.id'), nullable=True)  # Foreign Key to UserType
    image = Column(Text, default='', nullable=True)
    gender = Column(String(1), nullable=True)
    dob = Column(Date, nullable=True)
    calling_code = Column(String(10), nullable=True)
    phone = Column(String(20), default='', nullable=True)
    address = Column(Text, default='', nullable=True)
    pincode = Column(String(20), default='', nullable=True)
    country = Column(String(50), default='', nullable=True)
    state = Column(String(50), default='', nullable=True)
    city = Column(String(50), default='', nullable=True)
    isdeleted = Column(Boolean, default=False)
    createddate = Column(DateTime, default=datetime.utcnow, nullable=False)
    updateddate = Column(DateTime, nullable=True)

    # Relationship with UserType
    usertype = relationship('UserType', backref='users')

    def __repr__(self):
        return f'<User {self.username}>'

    def get_name(self):
        name = ""
        if self.first_name:
            name = f"{self.first_name}"
        if self.last_name:
            name = f"{name} {self.last_name}" if name else self.last_name
        return name

    def __str__(self):
        return f"{self.username}"


class Site(Base):
    __tablename__ = 'site'

    id = Column(Integer, primary_key=True)
    owner_user_id = Column(Integer, ForeignKey('auth_user.id'))
    sitename = Column(String(200))
    address = Column(Text, default='', nullable=True)
    country = Column(String(50), default='', nullable=True)
    state = Column(String(50), default='', nullable=True)
    city = Column(String(50), default='', nullable=True)
    latitude = Column(String(20), default='', nullable=True)
    longitude = Column(String(20), default='', nullable=True)
    isdeleted = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    createddate = Column(DateTime, default=datetime.utcnow)
    updateddate = Column(DateTime, nullable=True)

    owner_user = relationship('User', backref='sites')

    def __str__(self):
        return self.sitename


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('auth_user.id'), nullable=True)
    site_info_id = Column(Integer, ForeignKey('site.id'), nullable=True)
    joiningdate = Column(Date, nullable=True)
    min_wages = Column(Float, default=0.0)
    qualification = Column(String(250), default='')
    is_on_leave = Column(Boolean, default=False)
    isdeleted = Column(Boolean, default=False)
    createddate = Column(DateTime, default=datetime.utcnow)
    updateddate = Column(DateTime, nullable=True)

    user = relationship('User', backref='employee')
    site_info = relationship('Site', backref='employees')

    def __str__(self):
        return f"{self.user.username}"


class Attendance(Base):
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=True)
    site_info_id = Column(Integer, ForeignKey('site.id'), nullable=True)
    attendance = Column(String(2), nullable=True)  # Choices: 'P', 'A', 'HD', 'OT'
    date = Column(Date, nullable=True)
    isdeleted = Column(Boolean, default=False)
    createddate = Column(DateTime, default=datetime.utcnow)
    updateddate = Column(DateTime, nullable=True)

    employee = relationship('Employee', backref='attendances')
    site_info = relationship('Site', backref='attendances')

    def __str__(self):
        return f"{self.employee}"


class Leave(Base):
    __tablename__ = 'leave'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=True)
    site_info_id = Column(Integer, ForeignKey('site.id'), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    reason = Column(Text, nullable=True)
    isdeleted = Column(Boolean, default=False)
    createddate = Column(DateTime, default=datetime.utcnow)
    updateddate = Column(DateTime, nullable=True)

    employee = relationship('Employee', backref='leaves')
    site_info = relationship('Site', backref='leaves')

    def __str__(self):
        return f"{self.employee.id}"
