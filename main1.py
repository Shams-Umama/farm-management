from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user

local_server= True #SETTING UP LOCAL SERVER
app = Flask(__name__) #CREATE AN INSTANCE OF FLASK WEB APP
app.secret_key='abcxyz'

# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#config the database
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@127.0.0.1:3307/farmer'
db=SQLAlchemy(app) #INITIALIZING THE DATABASE, CONNECTS FLASK APP AND SQLALCHEMY 




#CREATING TABLES
class User(UserMixin,db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(35),nullable=False)
    email=db.Column(db.String(30),unique=True)
    password=db.Column(db.String(1000),nullable=False)

class Register(db.Model):
    rid=db.Column(db.Integer,primary_key=True)
    farmername=db.Column(db.String(50))
    adharnumber=db.Column(db.String(50))
    age=db.Column(db.Integer)
    gender=db.Column(db.String(50))
    phonenumber=db.Column(db.Integer)
    address=db.Column(db.Integer)
    farmingtype=db.Column(db.String(50))

class Farming(db.Model):
    fid=db.Column(db.Integer,primary_key=True)
    farmingtype=db.Column(db.String(100))

class Products(db.Model):
    pid=db.Column(db.Integer,primary_key=True)
    productname=db.Column(db.String(50))
    productdesc=db.Column(db.String(50))
    price=db.Column(db.Integer)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50))



@app.route('/', methods=['POST','GET'])
def home():
        if request.method == "POST": 
             return render_template("signup.html")
        return render_template("home.html")

@app.route('/signup',methods=['POST','GET'])
def signup(): 
    if request.method == "POST": 
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            print("Email already exists")
            return render_template('/signup.html') 
        encpassword=generate_password_hash(password)
        #new_user = db.engine.execute( f"INSERT INTO 'User'('username','email','password'))VALUES('{username}','{email}',' {encpassword}')")
        newuser=User(username=username,email=email,password=encpassword)
        db.session.add(newuser)
        db.session.commit()
      
        return render_template("login.html")

    return render_template('signup.html') 


@app.route('/login',methods=['POST','GET'])
def login(): 
    if request.method == "POST": 
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if check_password_hash(user.password,password):
            login_user(user)
           
            return render_template('home2.html')  #you can also use "return redirect(url_for('home2'))"
        else:
           
            return render_template('login.html')    
    return render_template('login.html') 


             

@app.route('/home2')
def home2():
     return render_template("home2.html")

@app.route('/register',methods=['POST','GET'])
@login_required
def register():
    farming=Farming.query.all() #Take all the values from farming table
    if request.method=="POST":
        farmername=request.form.get('farmername')
        adharnumber=request.form.get('adharnumber')
        age=request.form.get('age')
        gender=request.form.get('gender')
        phonenumber=request.form.get('phonenumber')
        address=request.form.get('address')
        farmingtype=request.form.get('farmingtype')     
        query=Register(farmername=farmername,adharnumber=adharnumber,age=age,gender=gender,phonenumber=phonenumber,address=address,farmingtype=farmingtype)
        db.session.add(query)
        db.session.commit()
        return redirect('/details')
    return render_template('register.html',farming=farming) #variable farming = table farming (we use it in register page)

@app.route('/details')
@login_required
def farmerdetails():
    # query=db.engine.execute(f"SELECT * FROM `register`") 
    query=Register.query.all()
    return render_template('details.html',query=query)

@app.route('/farming')
@login_required
def farming():
     return render_template("farming.html")

@app.route("/logout")
@login_required #only if the user is logged in, he/she is allowed to logout
def logout():
     return render_template('home.html')

@app.route('/add',methods=['POST','GET'])
def add():
    if request.method=="POST":
           username = request.form.get('username')
           email = request.form.get('email')
           productname = request.form.get('productname')
           productdesc = request.form.get('productdesc')
           price = request.form.get('price')
           query = Products(productname=productname,productdesc=productdesc,price=price,username=username,email=email)
           db.session.add(query)
           db.session.commit()
           return render_template("products.html")
     
    return render_template("add.html")

@app.route('/products')
def products():
     query=Products.query.all()
     return render_template("products.html",query=query)

@app.route('/edit/<int:rid>',methods=['POST','GET'])
def edit(rid):
        if request.method=="POST":
            farmername=request.form.get('farmername')
            adharnumber=request.form.get('adharnumber')
            age=request.form.get('age')
            gender=request.form.get('gender')
            phonenumber=request.form.get('phonenumber')
            address=request.form.get('address')
            farmingtype=request.form.get('farmingtype')     
            # query=db.engine.execute(f"UPDATE `register` SET `farmername`='{farmername}',`adharnumber`='{adharnumber}',`age`='{age}',`gender`='{gender}',`phonenumber`='{phonenumber}',`address`='{address}',`farming`='{farmingtype}'")
            post=Register.query.filter_by(rid=rid).first()
            print(post.farmername)
            post.farmername=farmername
            post.adharnumber=adharnumber
            post.age=age
            post.gender=gender
            post.phonenumber=phonenumber
            post.address=address
            post.farming=farmingtype
            db.session.commit()
            return redirect('/details')
        
        posts=Register.query.filter_by(rid=rid).first()
        Farming=Register.query.all()
        return render_template('edit.html',posts=posts,farming=farming)

@app.route("/delete/<int:rid>",methods=['POST','GET'])
@login_required
def delete(rid):
    #db.engine.execute(f"DELETE FROM `register` WHERE `register`.`rid`={rid}")
    post=Register.query.filter_by(rid=rid).first()
    db.session.delete(post)
    db.session.commit()
    flash("Slot Deleted Successful","warning")
    return redirect('/details')



@app.route('/farming',methods=['POST','GET'])
@login_required
def addfarming():
    if request.method=="POST":
        farmingtype=request.form.get('farmingtype')
        query=Farming.query.filter_by(farmingtype=farmingtype).first()
        if query:
            #flash("Farming Type Already Exist","warning")
            return redirect('/farming')
        dep=Farming(farmingtype=farmingtype)
        db.session.add(dep)
        db.session.commit()
        flash("farming type added","primary")
        
    return render_template('farming.html')

  



app.run(debug=True)