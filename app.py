from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

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

# class Sample(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))

#     def __repr__(self):
#         return '<Task %r>' % self.id

# stuff for db initialization
# with app.app_context():
#     db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM appointments WHERE hospitalname='The Medical City'")
        results = cur.fetchall()
        cur.close()

        # items = Sample.query.order_by(Sample.date_added).all()
        return render_template('index.html', items = results)

@app.route('/add/<apptid>', methods=['POST'])
def add():
    item_to_delete = Sample.query.get_or_404(id)
    
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Something went wrong with adding that item'

@app.route('/delete/<int:id>')
def delete(id):
    item_to_delete = Sample.query.get_or_404(id)
    
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Something went wrong with the deletion of that item'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    item = Sample.query.get_or_404(id)

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