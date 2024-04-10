from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime

from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'ccscloud.dlsu.edu.ph'
app.config['MYSQL_PORT'] = 20201
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'H2yPm49GvUWgAcuw38sphQ7f'
app.config['MYSQL_DB'] = 'mco2_final'

db = MySQL(app)


def format_time(input):
    html_datetime = datetime.fromisoformat(input)
    mysql_datetime_str = html_datetime.strftime('%Y-%m-%d %H:%M:%S')

    return mysql_datetime_str


@app.route('/', methods=['POST', 'GET'])
def index():
    
    query = request.form.get('query')
    cur = db.connection.cursor()

    if query:
        cur.execute(query)
    else:
        cur.execute("SELECT * FROM appointments WHERE City='Santa Cruz'")

    results = cur.fetchall()
    cur.close()

    return render_template('index.html', items = results, porty = app.config['MYSQL_PORT'])

@app.route('/add', methods=['POST', 'GET'])
def add():
    
    if request.method == 'POST':
        pxid = request.form['pxid']
        clinicid = request.form['clinicid']
        doctorid = request.form['doctorid']
        apptid = request.form['apptid']
        status = request.form['status']
        timequeued = request.form['timequeued']
        queuedate = request.form['queuedate']
        starttime = request.form['starttime']
        endtime = request.form['endtime']
        type = request.form['type']
        virtual = request.form['virtual']
        hospitalname = request.form['hospitalname']
        ishospital = request.form['ishospital']
        city = request.form['city']
        province = request.form['province']
        regionname = request.form['regionname']
        mainspecialty = request.form['mainspecialty']
        doctor_age = request.form['doctor_age']
        px_age = request.form['px_age']
        gender = request.form['gender']

        timequeued = format_time(timequeued)
        queuedate = format_time(queuedate)
        starttime = format_time(starttime)
        endtime = format_time(endtime)

        try:
            cur = db.connection.cursor()
            cur.execute(f"INSERT INTO appointments\
                        VALUES ('{pxid}','{clinicid}','{doctorid}','{apptid}','{status}','{timequeued}','{queuedate}',\
                            '{starttime}','{endtime}','{type}','{virtual}','{hospitalname}','{ishospital}','{city}',\
                            '{province}','{regionname}','{mainspecialty}',{doctor_age},{px_age},'{gender}')")
            cur.close()

            db.connection.commit()
            return redirect('/')
        
        except:
            return 'Something went wrong with adding that item'
        
    else:
        return render_template('add.html')

@app.route('/delete/<string:apptid>')
def delete(apptid):
    
    try:
        cur = db.connection.cursor()
        cur.execute(f"DELETE FROM appointments WHERE apptid='{apptid}'")
        cur.close()

        db.connection.commit()

        return redirect('/')
    except:
        return 'Something went wrong with the deletion of that item'

@app.route('/update/<string:upd_id>', methods=['GET', 'POST'])
def update(upd_id):

    cur = db.connection.cursor()
    cur.execute(f"SELECT * FROM appointments WHERE apptid = '{upd_id}'")
    appt_to_update = cur.fetchall()
    cur.close()

    if request.method == 'POST':
        pxid = request.form['pxid']
        clinicid = request.form['clinicid']
        doctorid = request.form['doctorid']
        apptid = request.form['apptid']
        status = request.form['status']
        timequeued = request.form['timequeued']
        queuedate = request.form['queuedate']
        starttime = request.form['starttime']
        endtime = request.form['endtime']
        type = request.form['type']
        virtual = request.form['virtual']
        hospitalname = request.form['hospitalname']
        ishospital = request.form['ishospital']
        city = request.form['city']
        province = request.form['province']
        regionname = request.form['regionname']
        mainspecialty = request.form['mainspecialty']
        doctor_age = request.form['doctor_age']
        px_age = request.form['px_age']
        gender = request.form['gender']

        timequeued = format_time(timequeued)
        queuedate = format_time(queuedate)
        starttime = format_time(starttime)
        endtime = format_time(endtime)

        try:
            cur = db.connection.cursor()
            cur.execute(f"UPDATE appointments\
                        SET pxid='{pxid}',clinicid='{clinicid}',doctorid='{doctorid}',apptid='{apptid}',status='{status}',\
                            timequeued='{timequeued}',queuedate='{queuedate}',starttime='{starttime}',endtime='{endtime}',\
                            type='{type}',`virtual`='{virtual}',hospitalname='{hospitalname}',ishospital='{ishospital}',\
                            city='{city}',province='{province}',regionname='{regionname}',mainspecialty='{mainspecialty}',\
                            doctor_age={doctor_age},px_age={px_age},gender='{gender}'\
                        WHERE apptid='{upd_id}'")
            cur.close()

            db.connection.commit()
            return redirect('/')
        
        except:
            return 'Something went wrong with updating that item'
        
    else:
        return render_template('update.html', item = appt_to_update[0])

@app.route('/update_port', methods=['GET', 'POST'])
def update_port():
    port = request.form.get('port')
    port = int(port)
    if port:
        app.config['MYSQL_PORT'] = port
        print(f'Port updated to {port}')
    else:
        return 'No port specified'
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)