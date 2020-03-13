from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/bank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
import os
app.config['UPLOAD_FOLDER']=os.getcwd()+"\\empimages\\"
db = SQLAlchemy(app)


class Emp(db.Model):
    empId = db.Column('emp_id',db.Integer(),primary_key=True)
    empName = db.Column('emp_name',db.String(50))
    empSal = db.Column('emp_sal', db.Float())
    empAge = db.Column('emp_age', db.Integer())
    emppic =  db.Column('emp_pic',db.String(256),nullable=True,default='NA')

    @staticmethod
    def dummyemp():
        return Emp(empId=0,empName='',empSal=0.0,empAge=0)

db.create_all()


''' hibyeee
=======
#pp
