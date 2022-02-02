from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user


# MY db connection
local_server= True
app = Flask(__name__)
app.secret_key='harshithbhaskar'


# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.user_loader
def customer_load_user(user_id):
    return customer.query.get(int(user_id))

# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databas_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/farm'
db=SQLAlchemy(app)

# here we will create db models that is tables
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))

class Farming(db.Model):
    fid=db.Column(db.Integer,primary_key=True)
    farmingtype=db.Column(db.String(100))


class Addagroproducts(db.Model):
    username=db.Column(db.String(50))
    email=db.Column(db.String(50))
    pid=db.Column(db.Integer,primary_key=True)
    productname=db.Column(db.String(100))
    productdesc=db.Column(db.String(300))
    price=db.Column(db.Integer)
    quantity = db.Column(db.Integer)


class purchase(db.Model):
    farmername=db.Column(db.String(50))
    oid=db.Column(db.Integer,primary_key=True)
    pid=db.Column(db.Integer)
    productname=db.Column(db.String(100))
    price=db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    phonenumber = db.Column(db.Integer)

class Trig(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    fid=db.Column(db.String(100))
    action=db.Column(db.String(100))
    timestamp=db.Column(db.String(100))


class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))

class Register(db.Model):
    rid=db.Column(db.Integer,primary_key=True)
    farmername=db.Column(db.String(50))
    adharnumber=db.Column(db.String(50))
    age=db.Column(db.Integer)
    gender=db.Column(db.String(50))
    phonenumber=db.Column(db.String(50))
    address=db.Column(db.String(50))
    farming=db.Column(db.String(50))
class adminuser(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))
    
class customer(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))
    

@app.route('/')
def index(): 
    return render_template('index.html')
@app.route('/admin')
def adminindex(): 
    return render_template('adminindex.html')

@app.route('/customer')
def customerindex(): 
    return render_template('customerindex.html')


@app.route('/farmerdetails')
@login_required
def farmerdetails():
    query=db.engine.execute(f"CALL sample1()") 
    return render_template('farmerdetails.html',query=query)

@app.route('/adminfarmerdetails')
@login_required
def adminfarmerdetails():
    query=db.engine.execute(f"CALL sample1()") 
    return render_template('adminfarmerdetails.html',query=query)

# @app.route('/normalfarmerdetails')
# @login_required
# def normalfarmerdetails():
#     query=db.engine.execute(f"CALL sample1()") 
#     return render_template('farmerdetails copy.html',query=query)

@app.route('/addingprod')
@login_required
def addingprod():
    query=db.engine.execute(f"SELECT * FROM `register`") 
    return render_template('addingprod.html',query=query)


@app.route('/agroproducts')
def agroproducts():
    query=db.engine.execute(f"SELECT * FROM `addagroproducts`") 
    return render_template('agroproducts.html',query=query)

@app.route('/customeragroproducts')
def customeragroproducts():
    query=db.engine.execute(f"SELECT * FROM `addagroproducts`") 
    return render_template('customeragroproducts.html',query=query)

@app.route('/adminagroproducts')
def adminagroproducts():
    query=db.engine.execute(f"SELECT * FROM `addagroproducts`") 
    return render_template('adminagroproducts.html',query=query)

@app.route('/addagroproduct',methods=['POST','GET'])
@login_required
def addagroproduct():
    if request.method=="POST":
        username=request.form.get('username')
        email=request.form.get('email')
        productname=request.form.get('productname')
        productdesc=request.form.get('productdesc')
        price=request.form.get('price')
        quantity = request.form.get('quantity')
        products=Addagroproducts(username=username,email=email,productname=productname,productdesc=productdesc,price=price,quantity=quantity)
        db.session.add(products)
        db.session.commit()
        flash("Product Added","info")
        return redirect('/agroproducts')
   
    return render_template('addagroproducts.html')

@app.route('/adminaddagroproduct',methods=['POST','GET'])
@login_required
def adminaddagroproduct():
    if request.method=="POST":
        username=request.form.get('username')
        email=request.form.get('email')
        productname=request.form.get('productname')
        productdesc=request.form.get('productdesc')
        price=request.form.get('price')
        quantity = request.form.get('quantity')
        products=Addagroproducts(username=username,email=email,productname=productname,productdesc=productdesc,price=price,quantity=quantity)
        db.session.add(products)
        db.session.commit()
        flash("Product Added","info")
        return redirect('/adminagroproducts')
   
    return render_template('adminaddagroproducts.html')

@app.route('/triggers')
 
def triggers():
    query=db.engine.execute(f"SELECT * FROM `trig`") 
    return render_template('triggers.html',query=query)

@app.route('/addfarming',methods=['POST','GET'])
@login_required
def addfarming():
    if request.method=="POST":
        farmingtype=request.form.get('farming')
        query=Farming.query.filter_by(farmingtype=farmingtype).first()
        if query:
            flash("Farming Type Already Exist","warning")
            return redirect('/addfarming')
        dep=Farming(farmingtype=farmingtype)
        db.session.add(dep)
        db.session.commit()
        flash("Farming Added","success")
    return render_template('farming.html')

@app.route('/adminaddfarming',methods=['POST','GET'])
@login_required
def normaladdfarming():
    if request.method=="POST":
        farmingtype=request.form.get('farming')
        query=Farming.query.filter_by(farmingtype=farmingtype).first()
        if query:
            flash("Farming Type Already Exist","warning")
            return redirect('/adminaddfarming')
        dep=Farming(farmingtype=farmingtype)
        db.session.add(dep)
        db.session.commit()
        flash("Farming Added","success")
    return render_template('adminfarming.html')




@app.route("/delete/<string:rid>",methods=['POST','GET'])
@login_required
def delete(rid):
    db.engine.execute(f"DELETE FROM `register` WHERE `register`.`rid`={rid}")
    flash("Slot Deleted Successful","danger")
    return redirect('/adminfarmerdetails')


@app.route("/edit/<string:rid>",methods=['POST','GET'])
@login_required
def edit(rid):
    farming=db.engine.execute("SELECT * FROM `farming`")
    posts=Register.query.filter_by(rid=rid).first()
    if request.method=="POST":
        farmername=request.form.get('farmername')
        adharnumber=request.form.get('adharnumber')
        age=request.form.get('age')
        gender=request.form.get('gender')
        phonenumber=request.form.get('phonenumber')
        address=request.form.get('address')
        farmingtype=request.form.get('farmingtype')     
        query=db.engine.execute(f"UPDATE `register` SET `farmername`='{farmername}',`adharnumber`='{adharnumber}',`age`='{age}',`gender`='{gender}',`phonenumber`='{phonenumber}',`address`='{address}',`farming`='{farmingtype}'")
        flash("Slot is Updates","success")
        return redirect('/farmerdetails')
    
    return render_template('edit.html',posts=posts,farming=farming)

@app.route("/adminedit/<string:rid>",methods=['POST','GET'])
@login_required
def adminedit(rid):
    farming=db.engine.execute("SELECT * FROM `farming`")
    posts=Register.query.filter_by(rid=rid).first()
    if request.method=="POST":
        farmername=request.form.get('farmername')
        adharnumber=request.form.get('adharnumber')
        age=request.form.get('age')
        gender=request.form.get('gender')
        phonenumber=request.form.get('phonenumber')
        address=request.form.get('address')
        farmingtype=request.form.get('farmingtype')     
        query=db.engine.execute(f"UPDATE `register` SET `farmername`='{farmername}',`adharnumber`='{adharnumber}',`age`='{age}',`gender`='{gender}',`phonenumber`='{phonenumber}',`address`='{address}',`farming`='{farmingtype}'")
        flash("Slot is Updates","success")
        return redirect('/adminfarmerdetails')
    
    return render_template('adminedit.html',posts=posts,farming=farming)



@app.route("/purchase/<string:pid>",methods=['POST','GET'])
@login_required
def purchase(pid):
    farming=db.engine.execute("SELECT * FROM `addagroproducts`")
    posts=Addagroproducts.query.filter_by(pid=pid).first()
    if request.method=="POST":
        farmername=request.form.get('username')
        productname=request.form.get('productname')
        price=request.form.get('price')
        quantity=request.form.get('quantity')
        phonenumber=request.form.get('phonenumber')
        
             
        query=db.engine.execute(f"INSERT INTO `purchase` (`username`,`email`,`pid`,`productname`,`price`,`quantity`) VALUES ('{farmername}','{phonenumber}','{pid}','{productname}','{price}','{quantity}')")
        flash("Slot is Updates","success")
        return redirect('/customeragroproducts')
    
    return render_template('purchase.html',posts=posts,farming=farming)


# @app.route('/signup',methods=['POST','GET'])
# def signup():
    # if request.method == "POST":
    #     username=request.form.get('username')
    #     email=request.form.get('email')
    #     password=request.form.get('password')
    #     print(username,email,password)
    #     user=User.query.filter_by(email=email).first()
    #     if user:
    #         flash("Email Already Exist","warning")
    #         return render_template('/signup.html')
    #     encpassword=generate_password_hash(password)

    #     new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

    #     # this is method 2 to save data in db
    #     # newuser=User(username=username,email=email,password=encpassword)
    #     # db.session.add(newuser)
    #     # db.session.commit()
    #     flash("Signup Succes Please Login","success")
    #     return render_template('login.html')

# @app.route('/signup',methods=['POST','GET'])
# def signup():
#     if request.method == "POST":
#         username=request.form.get('username')
#         email=request.form.get('email')
#         password=request.form.get('password')
#         print(username,email,password)
#         user=User.query.filter_by(email=email).first()
#         if user:
#             flash("Email Already Exist","warning")
#             return render_template('/signup.html')
#         encpassword=generate_password_hash(password)

#         new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

#         # this is method 2 to save data in db
#         # newuser=User(username=username,email=email,password=encpassword)
#         # db.session.add(newuser)
#         # db.session.commit()
#         flash("Signup Succes Please Login","success")
#         return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        print(username, email, password)
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist", "warning")
            return render_template('/signup.html')
        encpassword = generate_password_hash(password)

        new_user = db.engine.execute(
            f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        # newuser=User(username=username,email=email,password=encpassword)
        # db.session.add(newuser)
        # db.session.commit()
        flash("Signup Succes Please Login", "success")
        return render_template('login.html')

    return render_template('signup.html')




@app.route('/customersignup',methods=['POST','GET'])
def customersignup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        print(username,email,password)
        user=customer.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/customersignup.html')
        encpassword=generate_password_hash(password)

        new_user=db.engine.execute(f"INSERT INTO `customer` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        # newuser=User(username=username,email=email,password=encpassword)
        # db.session.add(newuser)
        # db.session.commit()
        flash("Signup Succes Please Login","success")
        return render_template('customerlogin.html')


    return render_template('customersignup.html')

@app.route('/adminsignup',methods=['POST','GET'])
def adminsignup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        print(username,email,password)
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/adminsignup.html')
        encpassword=generate_password_hash(password)

        new_user=db.engine.execute(f"INSERT INTO `adminuser` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        # newuser=User(username=username,email=email,password=encpassword)
        # db.session.add(newuser)
        # db.session.commit()
        flash("Signup Succes Please Login","success")
        return render_template('adminlogin.html')

          

    return render_template('adminsignup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')    

    return render_template('login.html')

@app.route('/customerlogin',methods=['POST','GET'])
def customerlogin():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=customer.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return render_template("customerindex.html")
        else:
            flash("invalid credentials","danger")
            return render_template('customerlogin.html')    

    return render_template('customerlogin.html')

@app.route('/adminlogin',methods=['POST','GET'])
def adminlogin():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=adminuser.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            
            return render_template("adminindex.html")
        else:
            flash("invalid credentials","danger")
            return render_template('adminlogin.html')    

    return render_template('adminlogin.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))

@app.route('/adminlogout')
@login_required
def adminlogout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('adminlogin'))

@app.route('/customerlogout')
@login_required
def customerlogout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('customerlogin'))



@app.route('/register',methods=['POST','GET'])
@login_required
def register():
    farming=db.engine.execute("SELECT * FROM `farming`")
    if request.method=="POST":
        farmername=request.form.get('farmername')
        adharnumber=request.form.get('adharnumber')
        age=request.form.get('age')
        gender=request.form.get('gender')
        phonenumber=request.form.get('phonenumber')
        address=request.form.get('address')
        farmingtype=request.form.get('farmingtype')     
        query=db.engine.execute(f"INSERT INTO `register` (`farmername`,`adharnumber`,`age`,`gender`,`phonenumber`,`address`,`farming`) VALUES ('{farmername}','{adharnumber}','{age}','{gender}','{phonenumber}','{address}','{farmingtype}')")
        flash("Your Record Has Been Saved","success")
        return redirect('/farmerdetails')
    return render_template('farmer.html',farming=farming)


@app.route('/adminregister',methods=['POST','GET'])

def adminregister():
    farming=db.engine.execute("SELECT * FROM `farming`")
    if request.method=="POST":
        farmername=request.form.get('farmername')
        adharnumber=request.form.get('adharnumber')
        age=request.form.get('age')
        gender=request.form.get('gender')
        phonenumber=request.form.get('phonenumber')
        address=request.form.get('address')
        farmingtype=request.form.get('farmingtype')     
        query=db.engine.execute(f"INSERT INTO `register` (`farmername`,`adharnumber`,`age`,`gender`,`phonenumber`,`address`,`farming`) VALUES ('{farmername}','{adharnumber}','{age}','{gender}','{phonenumber}','{address}','{farmingtype}')")
        flash("Your Record Has Been Saved","success")
        return redirect('/adminfarmerdetails')
    return render_template('adminfarmer.html',farming=farming)


# @app.route('/normalregister',methods=['POST','GET'])
# @login_required
# def normalregister():
#     farming=db.engine.execute("SELECT * FROM `farming`")
#     if request.method=="POST":
#         farmername=request.form.get('farmername')
#         adharnumber=request.form.get('adharnumber')
#         age=request.form.get('age')
#         gender=request.form.get('gender')
#         phonenumber=request.form.get('phonenumber')
#         address=request.form.get('address')
#         farmingtype=request.form.get('farmingtype')     
#         query=db.engine.execute(f"INSERT INTO `register` (`farmername`,`adharnumber`,`age`,`gender`,`phonenumber`,`address`,`farming`) VALUES ('{farmername}','{adharnumber}','{age}','{gender}','{phonenumber}','{address}','{farmingtype}')")
#         flash("Your Record Has Been Saved","success")
#         return redirect('/normalfarmerdetails')
#     return render_template('farmer copy.html',farming=farming)

@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'


app.run(debug=True)    