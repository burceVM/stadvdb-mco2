from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return '<Task %r>' % self.id

# stuff for db initialization
# with app.app_context():
#     db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        item_title = request.form['content']
        new_item = Sample(title=item_title)

        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/')
        except:
            return 'Something went wrong'

    else:
        items = Sample.query.order_by(Sample.date_added).all()
        return render_template('index.html', items = items)

@app.route('/delete/<int:id>')
def delete(id):
    item_to_delete = Sample.query.get_or_404(id)
    
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Something went wrong with the deletion of that hmm'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    item = Sample.query.get_or_404(id)

    if request.method == 'POST':
        item.title = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Something went wrong with updating :('
        
    else:
        return render_template('update.html', item = item)

if __name__ == "__main__":
    app.run(debug=True)