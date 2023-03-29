from flask import Flask, render_template, url_for, request, flash , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

#sqlite
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///erp.db'


#Initalize database
db=SQLAlchemy(app)

#Create database model
class Erp(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(200), nullable= False)
    number = db.Column(db.Integer, nullable= False)
    date_created = db.Column(db.DateTime, default= datetime.utcnow)

    #Create function to return a string
    def __repr__(self):
        #return '<Name %r>' % self.id
        return f"{self.id}, {self.name}, {self.number}"


#Creating the model
with app.app_context():
    db.create_all()

#homepage route
@app.route("/")
@app.route('/homepage')
def home():
    erps = Erp.query.order_by(Erp.date_created)
    return render_template("homepage.html",erps=erps)



#create upload route
@app.route("/uploads", methods=['POST','GET'])
def uploads():
    if request.method == 'POST':
        names = request.form['nm'].title()
        numbers = request.form['num']
        new = Erp(name=names,number=numbers)
        #Push to database
        try:
            db.session.add(new)
            db.session.commit()
            return redirect(url_for('uploads'))
        except:
            return 'There was an error...'
    else:
        erps = Erp.query.order_by(Erp.date_created)
        return render_template('upload.html', erps=erps)



#create delete route
@app.route("/delete/<int:id>", methods=['POST','GET'] )     
def delete(id):
    delete = Erp.query.get_or_404(id)
    try:
        db.session.delete(delete)
        db.session.commit()
        return redirect(url_for('uploads'))
    except:  
        return "There was an error"



#create update route
@app.route("/update/<int:id>", methods=['POST','GET'] )
def update(id):
    updates = Erp.query.get_or_404(id)
    if request.method == 'POST':
        updates.name = request.form['nm'].title()
        updates.number = request.form['num']
        try:
            db.session.commit()
            return redirect(url_for('uploads'))
        except:
            return "There was a problem"
    else:
        return render_template('update.html',updates=updates)



#create search route
@app.route('/searching', methods=['POST', 'GET'])
def searching():
    if request.method == 'POST':
        search = request.form['searched']
        if search.isdigit():
            if int(search) in (range(1,10000)):
                search_id = int(search)
                return redirect(url_for('searchid',search_id=search_id))
        else:
            search_name = search.title()
            return redirect(url_for('searchname',search_name=search_name))
    else:
        return redirect(url_for('uploads'))



#search by name
@app.route('/searchname/<search_name>', methods=['POST', 'GET'])
def searchname(search_name):
        results = Erp.query.filter_by(name = search_name).all()
        if results:
            return render_template('search.html',results=results)
        else:
            return render_template('search.html',search_name=search_name)



#search by id
@app.route('/searchid/<search_id>', methods=['POST', 'GET'])
def searchid(search_id):
        results = Erp.query.filter_by(id = search_id).all()
        if results:
            return render_template('search.html',results=results)
        else:
            return render_template('search.html',search_id=search_id) 




if __name__ == "__main__":
    app.run(debug=True)



