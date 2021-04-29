from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import datetime
import locale

#SETTING_LANGUAGE
locale.setlocale(locale.LC_ALL,"turkish")

app = Flask(__name__, static_url_path='/static', template_folder='C:/Users/özay/Desktop/eem-413/templates')
app.secret_key = "myblog"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/özay/Desktop/eem-413/user.db"
db = SQLAlchemy(app)



class BlogUsers(db.Model):
   id = db.Column(db.Integer,primary_key = True)
   name = db.Column(db.String)
   username = db.Column(db.String)
   email = db.Column(db.String)
   password = db.Column(db.String)


# Kullanıcı Giriş Decorator'ı
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Please login to view this page.","danger")
            return redirect(url_for("login"))

    return decorated_function

# REGISTERING FORM
class RegisterForm(Form):
   name = StringField("İsim Soyisim",validators=[validators.Length(min=5,max=25,message="En az 5, en fazla 25 karakter uzunluğunda olmalı.")])
   username = StringField("Kullanıcı Adı",validators=[validators.Length(min=5,max=20,message="5 karakterden fazla,20 karakterden az olmalı")])
   email = StringField("Email Adresi",validators=[validators.Email(message = "Lütfen Geçerli Bir Email Adresi Girin...")])
   password = PasswordField("Parola",validators=[
      validators.DataRequired(message="Bu alan boş geçilemez."),
      validators.EqualTo(fieldname = "confirm",message="Parolanız uyuşmuyor!")
   ])
   confirm = PasswordField("Parola Doğrula")

# LOGIN FORM
class LoginForm(Form):
   username = StringField("Kullanıcı Adı",validators=[validators.Length(min=5,max=25,message="En az 5, en fazla 25 karakter uzunluğunda olmalı."),validators.DataRequired(message="Bu alan boş geçilemez.")])
   password = PasswordField("Parola",validators=[validators.DataRequired("Bu alan boş geçilemez.")])




#Kayıt Olma
@app.route("/register",methods = ["GET","POST"])
def register():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)


        user = BlogUsers(name = name,username = username,email = email,password = password)
        db.session.add(user)
        db.session.commit()



        flash("You Have Successfully Registered ...","success")
        return redirect(url_for("login"))
    else:
        return render_template("register.html",form = form)
    
# LOGIN FORM
class LoginForm(Form):
   username = StringField("Kullanıcı Adı",validators=[validators.Length(min=5,max=25,message="En az 5, en fazla 25 karakter uzunluğunda olmalı."),validators.DataRequired(message="Bu alan boş geçilemez.")])
   password = PasswordField("Parola",validators=[validators.DataRequired("Bu alan boş geçilemez.")])

#LOGIN
@app.route("/login",  methods = ["GET","POST"])

def login():
   form = LoginForm(request.form)

   if request.method == "POST" and form.validate():
      username = form.username.data
      password_entered = form.password.data

      result = BlogUsers.query.filter_by(username = username).first()

      if not result == None:
         #sözlük yapısında
         real_password = result.password
         name = result.name

         if sha256_crypt.verify(password_entered,real_password):
            flash("Hoşgeldin {}".format(name),"success")

            session["logged_in"] = True
            session["username"] = username


            return redirect(url_for("index"))
         else:
            flash("Parola Hatalı","danger")
            return redirect(url_for("login"))
         
      else:
         flash("Böyle bir kullanıcı yok","danger")
         return redirect(url_for("login"))
   else:
      return render_template("login.html",form=form)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/deney1")
@login_required
def deney1():
    return render_template("deney1.html")
@app.route("/deney2")
@login_required
def deney2():
    return render_template("deney2.html")
@app.route("/deney3")
@login_required
def deney3():
    return render_template("deney3.html")
@app.route("/deney4")
@login_required
def deney4():
    return render_template("deney4.html")

if __name__ == "__main__":
   db.create_all()
   app.run(debug = True) 

