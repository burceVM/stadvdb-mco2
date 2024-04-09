from flask import Flask, render_template, request, redirect
from datetime import datetime

from flask_mysqldb import MySQL

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)

app.config['MYSQL_HOST'] = 'ccscloud.dlsu.edu.ph'
app.config['MYSQL_PORT'] = 20201
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'H2yPm49GvUWgAcuw38sphQ7f'
app.config['MYSQL_DB'] = 'mco2'

db = MySQL(app)

# class Appointment(db.Model):
#     pxid = db.Column(db.String(32))
#     clinicid = db.Column(db.String(32))
#     doctorid = db.Column(db.String(32))
#     apptid = db.Column(db.String(32), primary_key=True)

#     title = db.Column(db.String(200), nullable=False)
#     date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))

#     def __repr__(self):
#         return '<Apt %r>' % self.apptid

# stuff for db initialization
# with app.app_context():
#     db.create_all()

def format_time(input):
    html_datetime = datetime.fromisoformat(input)
    mysql_datetime_str = html_datetime.strftime('%Y-%m-%d %H:%M:%S')

    return mysql_datetime_str

@app.route('/', methods=['POST', 'GET'])
def index():
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM appointments WHERE City='Santa Cruz'")
        results = cur.fetchall()
        cur.close()

        # items = Appointment.query.order_by(Appointment.date_added).all()
        return render_template('index.html', items = results)

@app.route('/add', methods=['POST', 'GET'])
def add():
    # item_to_delete = Appointment.query.get_or_404(id)
    
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

@app.route('/delete/<int:id>')
def delete(id):
    item_to_delete = Appointment.query.get_or_404(id)
    
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Something went wrong with the deletion of that item'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    item = Appointment.query.get_or_404(id)

    if request.method == 'POST':
        item.title = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Something went wrong with updating that item'
        
    else:
        return render_template('update.html', item = item)

if __name__ == "__main__":
    app.run(debug=True)