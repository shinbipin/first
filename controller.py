import logging
from logging.handlers import TimedRotatingFileHandler
from flask_withlogger.models import Emp,app,db
from flask import render_template as rt,request as req
import os
log = logging.getLogger(__name__)
log.setLevel(level=logging.DEBUG)

# to log output on console
sformatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(lineno)d - %(funcName)s')
streamH = logging.StreamHandler() #console
streamH.setFormatter(sformatter) # how to print--format the output
streamH.setLevel(level=logging.DEBUG)
log.addHandler(streamH)


# to log output in a file based on timeframe
trdformatter = logging.Formatter('%(name)s -%(asctime)s - %(levelname)s - %(message)s - %(lineno)d - %(funcName)s')
trfh = TimedRotatingFileHandler(os.getcwd()+'\\logs.log',
                                       when="m",
                                       backupCount=7)
trfh.setFormatter(trdformatter)
trfh.setLevel(level=logging.INFO)
log.addHandler(trfh)
#from werkzeug import secure_filename


@app.route('/scp/welcome/')
def welcome_page():

    log.info('inside welcome page..!')
    return rt('emp.html',emp = Emp.dummyemp(),employees= Emp.query.all())


@app.route('/scp/save/',methods=['POST'])
def save_emp_info():
        #req.args # in case data is coming in uri..-method get
    userinfo = req.form #normal textual info


    uservalues = ''
    for att,val in userinfo.items():
        uservalues += att +":"+val +"\n"
    log.info('user entered values -- '+uservalues)
    uploadedfile = req.files['pic']  # multimedia
    msg = ''
    try:
        emp = Emp(empName=userinfo['empnm'],empSal=userinfo['empsal'],empAge=userinfo['empage'])
        db.session.add(emp)
        db.session.commit()
    except BaseException as e:
        log.error('Problem in save'+str(e.args))
        msg = "Emp Not Saved..!"
    else:
        log.info('New Emp Identifier {}'.format(emp.empId))
        msg = "Emp saved Successfully...{}".format(emp.empId)

        # to save uploaded file..!

        emp.emppic = 'emp/'+str(emp.empId)+"_"+uploadedfile.filename
        db.session.commit() #only to update emp record pic -- path in db
        log.info('-----------'+uploadedfile.filename)
        log.info(uploadedfile)
        uploadedfile.save("static/"+emp.emppic) #save on local drive
        log.info('File saved ...')

        return  rt('emp.html',msg = msg,emp = Emp.dummyemp(),employees= Emp.query.all())



if __name__ == '__main__':
    app.run(debug=True)