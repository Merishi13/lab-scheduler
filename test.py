from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import random
import os
from werkzeug.exceptions import HTTPException
from datetime import datetime as dt

current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(
  current_dir, "labdata.sqlite3")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()


class Labs(db.Model):
  __tablename__ = 'labs'
  block = db.Column(db.String, primary_key=True)
  labs = db.Column(db.String, primary_key=True)
  occupied = db.Column(db.String)

class Login(db.Model):
  __tablename__ = 'login'
  username = db.Column(db.String, primary_key=True)
  password = db.Column(db.String)
  status = db.Column(db.String)

class Adminlogin(db.Model):
  __tablename__ = 'adminlogin'
  ausername = db.Column(db.String, primary_key=True)
  apassword = db.Column(db.String)
  status = db.Column(db.String)

class Request(db.Model):
  __tablename__ = 'request'
  username = db.Column(db.String, primary_key=True)
  name = db.Column(db.String)
  labno = db.Column(db.String, primary_key=True)
  hno = db.Column(db.String)
  purpose = db.Column(db.String)
  start = db.Column(db.String)
  end = db.Column(db.String)
  response = db.Column(db.String)
  flag = db.Column(db.String)

@app.route('/', methods=['GET', 'POST'])
def index():

  if request.method == 'GET':
    return render_template("index.html")

  if request.method == 'POST':
    today = dt.today()
    today1 = str(today)
    time = today1[11:13]
    if (time >= '16'):
        delreq = Request.query.filter_by().all()
        for deli in delreq:
            db.session.delete(deli)
        db.session.commit()
    username = request.form['username']
    password = request.form['password']
    user = Login.query.filter_by(username = username).first()
    adminlogin = Adminlogin.query.filter_by(ausername = username).first()
    if user == None:
        if adminlogin == None:
            return render_template("index.html",msg = "*Please Sign Up")
        else:
            if adminlogin.apassword == password:
                adminlogin.status = "loggedin"
                db.session.commit()
                return redirect(url_for('home',user = adminlogin.ausername))
            else:
                return render_template("index.html",msg = "*Passwords Does Not Match")
    if user.password == password:
        user.status = "loggedin"
        db.session.commit()
        return redirect(url_for('home',user = user.username))
    else:
        return render_template("index.html",msg = "*Passwords Does Not Match")
      
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    randnum  = random.randint(1000,9999)
    if request.method == 'GET':
        return render_template("signup.html",randnum = randnum)

    if request.method == 'POST':
        username = request.form['signname']
        password = request.form['signpassword']
        user = Login.query.filter_by(username = username).first()
        adminlogin = Adminlogin.query.filter_by(ausername = username).first()
        if user != None:
            if adminlogin != None:
                return render_template("signup.html",randnum = randnum,msg = "*User Already Exists")
            
        login = Login(username = username, password = password)
        db.session.add(login)
        db.session.commit()
        return render_template("index.html")

@app.route('/home/<user>', methods=['GET', 'POST'])
def home(user):
  labdata = Labs.query.all()
  login = Login.query.all()
  admindet = Adminlogin.query.all()
  req = Request.query.all()
  user1 = Login.query.filter_by(username = user).first()
  adminlogin = Adminlogin.query.filter_by(ausername = user).first()
  if request.method == 'GET':
      if user1 == None and adminlogin == None:
          return redirect(url_for('signup'))
      elif user1 == None:
          if adminlogin.status != 'loggedin':
              return redirect(url_for('index'))
          else:
              return render_template("home.html", labdata=labdata,block = "A",user = user,req = req,admindet = admindet,login = login)
      elif adminlogin == None:
          if user1.status != 'loggedin':
                 return redirect(url_for('index'))
          else:
              return render_template("home.html", labdata=labdata,block = "A",user = user,req = req,admindet = admindet,login = login)
              
  if request.method == 'POST':
         if user1 == None and adminlogin == None:
             return redirect(url_for('signup'))
         elif user1 == None:
             if adminlogin.status != 'loggedin':
                 return redirect(url_for('index'))
             else:
                 return render_template("home.html", labdata=labdata, block = "A",user = user,req = req,admindet = admindet,login = login)
                 
         elif adminlogin == None:
             if user1.status != 'loggedin':
                 return redirect(url_for('index'))
             else:
                 return render_template("home.html", labdata=labdata, block = "A",user = user,req = req,admindet = admindet,login = login)

@app.route('/home/<user>/<block>', methods=['GET', 'POST'])
def home1(user, block):
  login = Login.query.all()
  labdata = Labs.query.filter_by(block = block).all()
  admindet = Adminlogin.query.all()
  req = Request.query.all()
  user1 = Login.query.filter_by(username = user).first()
  adminlogin = Adminlogin.query.filter_by(ausername = user).first()
  if request.method == 'GET':
         if user1 == None and adminlogin == None:
             return redirect(url_for('signup'))
         elif user1 == None:
             if adminlogin.status != 'loggedin':
                 return redirect(url_for('index'))
             else:
                 return render_template("home.html", labdata=labdata,block = block,user = user,req = req,admindet = admindet,login = login)
         elif adminlogin == None:
             if user1.status != 'loggedin':
                 return redirect(url_for('index'))
             else:
                 return render_template("home.html", labdata=labdata,block = block,user = user,req = req,admindet = admindet,login = login)
  if request.method == 'POST':
      if user1 == None and adminlogin == None:
          return redirect(url_for('signup'))
      elif user1 == None:
          if adminlogin.status != 'loggedin':
              return redirect(url_for('index'))
          else:
              name = request.form["name"]
              labno = request.form['labno']
              hno = request.form['hno']
              pur = request.form['purpose']
              start = request.form['start']
              end = request.form['end']
              response = 'PENDING'
              req1 = Request(username = user, name = name, labno = block + labno, hno = hno, purpose = pur, start = start, end = end, response = response,flag = 'False')
              req2 = Request.query.filter_by(username = user).first()
              if req2 == None:
                  db.session.add(req1)
                  db.session.commit()
                  msg = ''
              else:
                  msg = '*YOU CANNOT BOOK A LAB TWICE'
                  
              return render_template("home.html", labdata=labdata,block = block, user = user,req = req,admindet = admindet,login = login,msg = msg) 
      elif adminlogin == None:
          if user1.status != 'loggedin':
              return redirect(url_for('index'))
          else:
              name = request.form["name"]
              labno = request.form['labno']
              hno = request.form['hno']
              pur = request.form['purpose']
              start = request.form['start']
              end = request.form['end']
              response = 'PENDING'
              req1 = Request(username = user, name = name, labno = block + labno, hno = hno, purpose = pur, start = start, end = end, response = response,flag = 'False')
              req2 = Request.query.filter_by(username = user).first()
              if req2 == None:
                  db.session.add(req1)
                  db.session.commit()
                  msg = ''
              else:
                  msg = '*YOU CANNOT BOOK A LAB TWICE'
                  
              return render_template("home.html", labdata=labdata,block = block, user = user,req = req,admindet = admindet,login = login,msg = msg)
          
          
          
@app.route('/<user>/<hno>/<lab>/reject', methods=['GET', 'POST'])
def reject(user,lab,hno):
    if request.method == 'POST':
        labdata = Labs.query.all()
        login = Login.query.all()
        admindet = Adminlogin.query.all()
        req = Request.query.all()
        rej = Request.query.filter_by(hno = hno,labno = lab).first()
        rej.response = 'REJECTED'
        rej.flag = 'True'
        db.session.commit()
        return redirect(url_for('home', user = user))

@app.route('/<user>/<hno>/<lab>/accept', methods=['GET', 'POST'])
def accept(user,lab,hno):
  labdata = Labs.query.all()
  login = Login.query.all()
  admindet = Adminlogin.query.all()
  req = Request.query.all()
  rej = Request.query.filter_by(hno = hno,labno = lab).first()
  rej.response = 'ACCEPTED'
  rej.flag = 'True'
  db.session.commit()
  return redirect(url_for('home', user = user))

@app.route('/logout/<user>' , methods=['GET', 'POST'])
def logout(user):
    user1 = Login.query.filter_by(username = user).first()
    adminlogin = Adminlogin.query.filter_by(ausername = user).first()
    if user1 == None:
        adminlogin.status = 'loggedout'
        db.session.commit()
    elif adminlogin == None:
        user1.status = 'loggedout'
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug = True)
