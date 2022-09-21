from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,DateTime,func
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager,UserMixin, login_user,login_required,logout_user,current_user
import os
import random
import urllib.request

app=Flask(__name__)
ENV='prod'

if ENV=='dev':
    app.debug=True
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost/teachers"
else:
    app.debug=False
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://ngphbicnonovun:97468d85c168eb91ebc17c6d468d73476bfbc699ed5f7c2dda18ab176f521049@ec2-3-224-184-9.compute-1.amazonaws.com:5432/dfn3d2la3ofkld"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =False
app.config['SECRET_KEY'] = 'cairocoders-ednalan'
UPLOAD_FOLDER = 'app/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024   
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
   
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
db = SQLAlchemy(app)

def populate_db():          
    titlelist = [Title(title="Mr"),Title(title="Mrs"),Title(title="Miss")]
    db.session.bulk_save_objects(titlelist)    
    aqflist = [Aqf_Levels(levels="Level-01"),Aqf_Levels(levels="Level-02"),Aqf_Levels(levels="Level-03"),Aqf_Levels(levels="Level-04"),Aqf_Levels(levels="Diploma"),Aqf_Levels(levels="Advanced Diploma"),Aqf_Levels(levels="Bachelor Degree"),Aqf_Levels(levels="Graduate Diploma"),Aqf_Levels(levels="Master Degree"),Aqf_Levels(levels="Doctorate")]
    db.session.bulk_save_objects(aqflist)
    semlist=[
    Semesters(semester_description="Semester 1| 28 February-24 June 2022"),
    Semesters(semester_description="Semester 2| 25 July–18 November"),
    Semesters(semester_description="Trimester 1| 28 February-3 June"),
    Semesters(semester_description="Trimester 2| 25 July–28 October"),
    Semesters(semester_description="Trimester 3| 7 November 2022–17 February 2023"),
    Semesters(semester_description="Session 1| 10 January–4 March"),
    Semesters(semester_description="Session 2| 7 March–29 April"),
    Semesters(semester_description="Session 3| 2 May-24 June"),
    Semesters(semester_description="Session 4| 6 June-29 July"),
    Semesters(semester_description="Session 5| 27 June–19 August"),
    Semesters(semester_description="Session 6| 22 August–14 October"),
    Semesters(semester_description="Session 7| 17 October–9 December"),
    Semesters(semester_description="Summer Session (Session 8)| 28 November 2022–3 February 2023")]
    db.session.bulk_save_objects(semlist)
    courselist=[
    Courses(course_description="BUS104 Discovering Management"),
    Courses(course_description="DES105 Design Methods"),
    Courses(course_description="ICT110 Introduction to Data Science"),
    Courses(course_description="ICT112 Programming Fundamentals"),
    Courses(course_description="ICT115 Introduction to Systems Design"),
    Courses(course_description="ICT120 Computer Networks"),
    Courses(course_description="SEC100 Foundations of Computer Security"),
    Courses(course_description="SCI110 Science Research Methods"),
    Courses(course_description="DES221 Introduction to Interactive Media"),
    Courses(course_description="DES222 Responsive Design and Wearable Technologies"),
    Courses(course_description="DIG202 Bringing Data to Life"),
    Courses(course_description="ENS253 Geographic Information Science and Technology"),
    Courses(course_description="ICT200 Systems Analysis and Design"),
    Courses(course_description="ICT211 Database Design"),
    Courses(course_description="ICT320 Database Programming"),
    Courses(course_description="ICT342 ICT Industry Project"),
    Courses(course_description="ICT351 ICT Professional Practice"),
    Courses(course_description="ICT352 Project Management"),
    Courses(course_description="SEC303 Device & Network Security"),
    Courses(course_description="CSC201 Data Structures and Algorithms"),
    Courses(course_description="CSC202 Mobile App Project"),
    Courses(course_description="ICT220 Wireless Communications"),
    Courses(course_description="ICT221 Object-Oriented Programming"),
    Courses(course_description="CSC301 Full Stack Web Development"),
    Courses(course_description="CSC302 Modelling and Testing"),
    Courses(course_description="CSC303 Cloud and DevOps"),
    Courses(course_description="DIG301 Artificial Intelligence: Implications for Organisations in the Digital Age"),
    Courses(course_description="SEC301 Cybersecurity"),
    Courses(course_description="SEC302 Ethics in Cyber Security"),
    Courses(course_description="SEC304 Cryptography, Blockchain and Information Security")]
    db.session.bulk_save_objects(courselist)    
    db.session.commit()    
    stafflist=Staff(title="Mr",first_name="Admin",last_name="Admin",uname="Admin",password=generate_password_hash("Admin"),address="Address",email="email@email.com",phone="123456789",role="Admin",isapproved=True)
    db.session.add(stafflist)
    db.session.commit()

@app.route('/signup', methods = ['GET','POST'])
def signup():
    if request.method == "POST":        
        #create variable for easy access
        role=request.form.get("role")
        title = request.form.get("title")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        uname = request.form.get("uname")
        password = request.form.get("password")
        _hashed_password=generate_password_hash(password)
        cpassword = request.form.get("cpassword")
        address = request.form.get("address")
        email = request.form.get("email")
        phone = request.form.get("phone")
        role  =request.form.get("role")
        print("ma yaha chu")
        isapproved = False if role=="Admin" else True        
        #check if username already exists       
        account=Staff.query.filter_by(uname=uname).first()
        if account:
            flash('Username already exists','Danger')
            return redirect(url_for("signin"))
        else:
            data=Staff(title=title,first_name=fname,last_name=lname,uname=uname,password=_hashed_password,role=role,address=address,email=email,phone=phone,isapproved=isapproved)
            db.session.add(data)
            db.session.commit()
            flash('Userid created successfully','success')
            return redirect(url_for("signin"))    
    else:
        tdata=Title.query.all()
        return render_template('signup.html',tdata=tdata)

#flask login stuff
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='signin'
@login_manager.user_loader
def load_user(staff_id):
    return Staff.query.get(int(staff_id))

#routes
@app.route('/', methods = ['GET','POST'])
@app.route('/signin', methods = ['GET','POST'])
def signin():
    if request.method == "POST":        
        uname = request.form.get("uname")
        password = request.form.get("password")            
        user=Staff.query.filter(Staff.uname==uname,Staff.isapproved==True).first()        
        if user is not None:
            print("password milyo")
            password_rs=user.password                    
            if check_password_hash(password_rs,password):            
                login_user(user)
                session['loggedin']=True                
                session['uname']=user.uname
                session['staff_id']=user.staff_id                
                session['role']= user.role             
                return redirect(url_for("gotodash"))
        else:
            flash("Invalid Username/Password/role",'Warning')         
            return render_template('signin.html')
    else:
        return render_template('signin.html')

@app.route('/gotodash')
@login_required
def gotodash():     
    if 'loggedin' in session:
        return render_template('dashboard.html')        
    else:
        return render_template('signin.html')   

@app.route('/mdetails', methods = ['GET','POST'])
@login_required
def mdetails():
    if request.method=='POST':
        title = request.form.get("title")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        address = request.form.get("address")
        email = request.form.get("email")
        phone = request.form.get("phone")
        avlstatus=Staff.query.filter_by(staff_id=session['staff_id']).count()               
        if avlstatus==0:  
            print("go to insert query")          
            data = Staff(staff_id=session['staff_id'],title=title,first_name=fname,last_name=lname,address=address,email=email,phone=phone)            
            db.session.add(data)
            db.session.commit()
            flash("Data Saved Successfully",'success')
            return redirect(url_for("mdetails"))
        else:
            print("go to update query")
            staff=Staff.query.filter_by(staff_id=session['user_id']).first()
            staff.title = title
            staff.first_name=fname       
            staff.last_name=lname
            staff.address=address
            staff.email=email
            staff.phone=phone
            db.session.commit()
            flash("Data Updated Successfully",'success')
            return redirect(url_for("mdetails"))
    else:
        adata=Aqf_Levels.query.all()        
        sadata = db.session.query(Qualification,Aqf_Levels
        ).filter(Qualification.staff_id==session['staff_id']
        ).join(Aqf_Levels,Qualification.aqf_id==Aqf_Levels.aqf_id       
        ).all() 
        print(sadata)   
        tdata=Title.query.all()        
        sdata=Staff.query.filter_by(staff_id=session['staff_id']).all()                       
        return render_template('staff_mdetails.html',sdata=sdata,tdata=tdata,adata=adata,sadata=sadata)

@app.route('/edit_mdetails/<int:staff_id>', methods = ['GET'])
@login_required
def edit_mdetails(staff_id):
    tdata=Title.query.all()    
    edata=Staff.query.filter_by(staff_id=staff_id).first()
    data=Staff.query.filter_by(staff_id=staff_id).all()
    return render_template('staff_mdetails_edit.html',data=data,edata=edata,tdata=tdata)

@app.route('/update_mdetails', methods = ['POST'])
@login_required
def update_mdetails():
    if request.method=='POST':
        staff_id=request.form.get("staff_id")        
        staff=Staff.query.filter_by(staff_id=staff_id).first()
        staff.title = request.form.get("title")
        staff.first_name=request.form.get("fname")     
        staff.last_name=request.form.get("lname")
        staff.address=request.form.get("address")
        staff.email=request.form.get("email")
        staff.phone=request.form.get("phone")
        db.session.commit()
        flash("Data Updated Successfully",'success')
        return redirect(url_for("mdetails")) 

@app.route('/qdetails', methods = ['POST'])
@login_required
def qdetails():
    if request.method=='POST':
        aqf_id=request.form.get("aqf_id")        
        avlstatus=Qualification.query.filter_by(staff_id=session['staff_id']).count()               
        if avlstatus==0:
            data = Qualification(staff_id=session['staff_id'],aqf_id=aqf_id)            
            db.session.add(data)
            db.session.commit()
            flash("Data Saved Successfully",'success')
            return redirect(url_for("mdetails"))
        else:
            qual=Qualification.query.filter_by(staff_id=session['staff_id']).first()
            qual.staff_id=session['staff_id']
            qual.aqf_id=aqf_id           
            db.session.commit()
            flash("Data Updated Successfully",'success')
            return redirect(url_for("mdetails"))

@app.route('/cdetails', methods = ['GET','POST'])
@login_required
def cdetails():
    if request.method=='POST':
        coursedescription = request.form.get("coursedescription")
        data = Courses(course_description=coursedescription)            
        db.session.add(data)
        db.session.commit()
        flash("Data Saved Successfully",'success')
        return redirect(url_for("cdetails"))
    else:
        data=Courses.query.all()
        return render_template('cdetails.html',data=data)

#route for editing courses        
@app.route('/edit_cdetails/<int:course_id>', methods = ['GET'])
@login_required
def edit_cdetails(course_id):
    edata=Courses.query.filter_by(course_id=course_id).first()    
    return render_template('cdetails_edit.html',edata=edata)

@app.route('/update_cdetails', methods = ['POST'])
@login_required
def update_cdetails():
    if request.method=='POST':
        course_id=request.form.get("course_id")        
        course=Courses.query.filter_by(course_id=course_id).first()
        course.course_description = request.form.get("course_description")        
        db.session.commit()
        flash("Data Updated Successfully",'success')
        return redirect(url_for("cdetails"))
 
@app.route('/sdetails', methods = ['GET','POST'])
@login_required
def sdetails():
    if request.method=='POST':
        semesterdescription = request.form.get("semester_description")
        data = Semesters(semester_description=semesterdescription)            
        db.session.add(data)
        db.session.commit()
        flash("Data Saved Successfully",'success')
        return redirect(url_for("sdetails"))
    else:
        data=Semesters.query.all()
        return render_template('sdetails.html',data=data)

#route for editing courses        
@app.route('/edit_sdetails/<int:semester_id>', methods = ['GET'])
@login_required
def edit_sdetails(semester_id):
    edata=Semesters.query.filter_by(semester_id=semester_id).first()
    print(edata)    
    return render_template('sdetails_edit.html',edata=edata)

@app.route('/update_sdetails', methods = ['POST'])
@login_required
def update_sdetails():
    if request.method=='POST':
        semester_id=request.form.get("semester_id")        
        semester=Semesters.query.filter_by(semester_id=semester_id).first()        
        semester.semester_description = request.form.get("semester_description")        
        db.session.commit()
        flash("Data Updated Successfully",'success')
        return redirect(url_for("sdetails"))  

@app.route('/calloc', methods = ['GET','POST'])
@login_required
def calloc():
    if session['role']=='Admin':
        if request.method=='POST':
            sid=request.form.get("semester_id")
            cid=request.form.get("course_id")
            avlstatus=Courses_Available.query.filter_by(semester_id=sid,course_id=cid).count()               
            if avlstatus==0:
                cadata=Courses_Available(semester_id=sid,course_id=cid)
                db.session.add(cadata)
                db.session.commit()
                flash("Data saved succesfully",'success')            
                return redirect(url_for("calloc"))
            else:
                flash("Semester Course combination already exists !",'warning')            
                return redirect(url_for("calloc"))
        else:
            semdata=Semesters.query.all()
            cordata=Courses.query.all()
            cadata = db.session.query(Courses_Available,Courses,Semesters        
            ).join(Courses,Courses_Available.course_id==Courses.course_id
            ).join(Semesters,Courses_Available.semester_id==Semesters.semester_id
            ).all()
            print(cadata)
            return render_template('calloc.html',semdata=semdata,cordata=cordata,cadata=cadata)    
    else:
        return redirect(url_for("gotodash"))
@app.route('/capply', methods = ['GET','POST'])
@login_required
def capply():
    if request.method=='POST':
        ca_id=request.form.get("ca_id")
        status=request.form.get("status")
        staff_id=session['staff_id']
        avlstatus=Staff_Teach_Courses.query.filter_by(ca_id=ca_id,staff_id=staff_id).count()               
        if avlstatus==0:
            stcdata=Staff_Teach_Courses(ca_id=ca_id,staff_id=staff_id,status=status)
            db.session.add(stcdata)
            db.session.commit()
            flash("Data saved succesfully",'success')            
            return redirect(url_for("capply"))
        else:
            flash("You have already applied for this course !",'warning')  
            return redirect(url_for("capply"))        
    else:
        stcdata = db.session.query(Staff_Teach_Courses,Courses_Available,Courses,Semesters,Staff 
        ).join(Courses_Available,Courses_Available.ca_id==Staff_Teach_Courses.ca_id               
        ).join(Courses,Courses_Available.course_id==Courses.course_id
        ).join(Semesters,Courses_Available.semester_id==Semesters.semester_id
        ).join(Staff,Staff_Teach_Courses.staff_id==Staff.staff_id
        ).filter(Staff_Teach_Courses.staff_id==session['staff_id']
        ).all()
        print (stcdata)
        cadata = db.session.query(Courses_Available,Courses,Semesters        
        ).join(Courses,Courses_Available.course_id==Courses.course_id
        ).join(Semesters,Courses_Available.semester_id==Semesters.semester_id
        ).all()
        return render_template('capply.html',cadata=cadata,stcdata=stcdata)

@app.route('/reqman', methods = ['GET','POST'])
@login_required
def reqman():
    if session['role']=='Admin':
        if request.method=='POST':
            stc_id=request.form.get("stc_id")
            remarks=request.form.get("remarks")
            status=request.form.get("status")
            approvedby=session['uname']
            stc=Staff_Teach_Courses.query.filter_by(stc_id=stc_id).first()
            stc.status = status
            stc.remarks = remarks
            stc.authorisedby = approvedby
            db.session.commit()
            flash("Data Updated Successfully",'success')
            return redirect(url_for("reqman"))
        else:
            pendingdata = db.session.query(Staff_Teach_Courses,Courses_Available,Courses,Semesters,Staff 
            ).join(Courses_Available,Courses_Available.ca_id==Staff_Teach_Courses.ca_id               
            ).join(Courses,Courses_Available.course_id==Courses.course_id
            ).join(Semesters,Courses_Available.semester_id==Semesters.semester_id
            ).join(Staff,Staff_Teach_Courses.staff_id==Staff.staff_id
            ).filter(Staff_Teach_Courses.status=='Pending'
            ).all()
            approveddata = db.session.query(Staff_Teach_Courses,Courses_Available,Courses,Semesters,Staff 
            ).join(Courses_Available,Courses_Available.ca_id==Staff_Teach_Courses.ca_id               
            ).join(Courses,Courses_Available.course_id==Courses.course_id
            ).join(Semesters,Courses_Available.semester_id==Semesters.semester_id
            ).join(Staff,Staff_Teach_Courses.staff_id==Staff.staff_id
            ).filter(Staff_Teach_Courses.status=='Approved'
            ).all()
            return render_template('reqman.html',pendingdata=pendingdata,approveddata=approveddata)    
    else:
        return redirect(url_for("gotodash"))
    
@app.route('/report/<int:staff_id>', methods = ['GET'])
@login_required
def report(staff_id):
    mdata=db.session.query(Staff,Qualification,Aqf_Levels 
    ).join(Qualification,Qualification.staff_id==Staff.staff_id               
    ).join(Aqf_Levels,Qualification.aqf_id==Aqf_Levels.aqf_id            
    ).filter(Staff.staff_id==staff_id
    ).all()
    print(mdata)
    return render_template('staff_report.html',mdata=mdata)

@app.route('/staffman', methods = ['GET','POST'])
@login_required
def staffman():
    return render_template('staff_man.html',mdata=mdata)

@app.route('/disable/<int:staff_id>', methods = ['GET','POST'])
@login_required
def disable(staff_id):
    staff=Staff.query.filter_by(staff_id=staff_id).first()        
    staff.isapproved=False
    db.session.commit()
    flash("Data Updated Successfully",'success')
    return redirect(url_for("staffman"))
    

@app.route('/enable/<int:staff_id>', methods = ['GET','POST'])
@login_required
def enable(staff_id):
    staff=Staff.query.filter_by(staff_id=staff_id).first()        
    staff.isapproved=True
    db.session.commit()
    flash("Data Updated Successfully",'success')
    return redirect(url_for("staffman"))

@app.route('/MakeTeacher/<int:staff_id>', methods = ['GET','POST'])
@login_required
def MakeTeacher(staff_id):
    staff=Staff.query.filter_by(staff_id=staff_id).first()        
    staff.role="Teacher"
    db.session.commit()
    flash("Data Updated Successfully",'success')
    return redirect(url_for("staffman"))
    

@app.route('/MakeAdmin/<int:staff_id>', methods = ['GET','POST'])
@login_required
def MakeAdmin(staff_id):
    staff=Staff.query.filter_by(staff_id=staff_id).first()        
    staff.role="Admin"
    db.session.commit()
    flash("Data Updated Successfully",'success')
    return redirect(url_for("staffman"))



@app.route('/logout',methods = ['GET','POST'])
@login_required
def logout():
    session.pop('loggedin',None)
    session.pop('user_id',None)
    session.pop('uname',None)
    session.pop('role',None)
    logout_user()
    flash('Logged out successfully','success')
    return redirect(url_for("signin"))

#create table structure

class Staff(db.Model,UserMixin):
    __tablename__ = 'staff'    
    staff_id = db.Column(db.Integer,primary_key=True)  
    title = db.Column(db.String(255))    
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    uname = db.Column(db.String(255),unique=True) 
    password = db.Column(db.String(255))    
    address=db.Column(db.String(255))
    email=db.Column(db.String(255))
    phone=db.Column(db.String(255))
    role = db.Column(db.String(255))
    isapproved=db.Column(db.Boolean,default=False) 

    def get_id(self):
           return (self.staff_id)

class Qualification(db.Model,UserMixin):
    __tablename__ = 'qualification'    
    staff_id = db.Column(db.Integer,db.ForeignKey('staff.staff_id'),primary_key=True)  
    aqf_id = db.Column(db.Integer,db.ForeignKey('aqf_level.aqf_id'))     

class Title(db.Model,UserMixin):
    __tablename__='title' 
    title_id= db.Column(db.Integer,primary_key=True)   
    title = db.Column(db.String(255))      

class Aqf_Levels(db.Model,UserMixin):
    __tablename__ = 'aqf_level'    
    aqf_id = db.Column(db.Integer,primary_key=True)
    levels = db.Column(db.String(255))

class Courses(db.Model,UserMixin):
    __tablename__ = 'courses'    
    course_id = db.Column(db.Integer,primary_key=True)
    course_description = db.Column(db.String(255))

class Semesters(db.Model,UserMixin):
    __tablename__ = 'semesters'    
    semester_id = db.Column(db.Integer,primary_key=True)
    semester_description = db.Column(db.String(255))

class Courses_Available(db.Model,UserMixin):
    __tablename__ = 'courses_available'
    ca_id = db.Column(db.Integer,primary_key=True)    
    semester_id = db.Column(db.Integer,db.ForeignKey('semesters.semester_id'))
    course_id = db.Column(db.Integer,db.ForeignKey('courses.course_id'))

class Staff_Teach_Courses(db.Model,UserMixin):
    __tablename__ = 'staff_teach_courses'
    stc_id = db.Column(db.Integer,primary_key=True)    
    ca_id= db.Column(db.Integer,db.ForeignKey('courses_available.ca_id'))
    staff_id= db.Column(db.Integer,db.ForeignKey('staff.staff_id'))
    status = db.Column(db.String(255))
    remarks = db.Column(db.String(255))
    authorisedby= db.Column(db.String(255))