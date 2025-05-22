from flask import Flask,render_template,redirect,request,flash,redirect,session, Response
import mysql.connector
import re
import os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import datetime
from fpdf import FPDF 



app=Flask(__name__)
app.config['upload_loc']="C:\\Users\\HP\\myproject\\venv\\static\\math"
app.secret_key="as"

# CODE FOR SQLALCHEMY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@localhost/siddhigiri'
db = SQLAlchemy(app)

class product(db.Model):
    
    productno = db.Column(db.Integer, primary_key=True,unique=True, nullable=False)
    name = db.Column(db.String(52), unique=False, nullable=True)
    pid = db.Column(db.String(10), unique=False, nullable=True)
    price = db.Column(db.String(10,2), unique=False, nullable=True)
    desci = db.Column(db.String(), unique=False, nullable=True)
    img = db.Column(db.String(20), unique=False, nullable=True)
    category= db.Column(db.String(20), unique=False, nullable=True)

class login(db.Model):
	id = db.Column(db.Integer, primary_key=True,unique=True, nullable=False)
	username = db.Column(db.String(52), unique=True, nullable=True)
	email = db.Column(db.String(50), unique=False, nullable=True)
	phone = db.Column(db.String(50), unique=False, nullable=True)
	password=db.Column(db.String(50), unique=False, nullable=True)


class nbooking(db.Model):
	bno = db.Column(db.Integer, primary_key=True,unique=True, nullable=False)
	
	date = db.Column(db.String(50), unique=False, nullable=True)
	name = db.Column(db.String(50), unique=False, nullable=True)
	phone = db.Column(db.String(50), unique=False, nullable=True)
	adhar = db.Column(db.String(50), unique=False, nullable=True)
	address=db.Column(db.String(50), unique=False, nullable=True)
	normal=db.Column(db.Integer(), unique=False, nullable=True)
	kids=db.Column(db.Integer(), unique=False, nullable=True)

class cart(db.Model):
	cartid = db.Column(db.Integer, primary_key=True,unique=True, nullable=False)
	pid=db.Column(db.Integer(), unique=False, nullable=True)
	cid=db.Column(db.Integer(), unique=False, nullable=True)
	qty=db.Column(db.Integer(), unique=False, nullable=True)
	rate=db.Column(db.Integer(), unique=False, nullable=True)


conn=mysql.connector.connect(host="localhost",user="root",password="mysql",database="siddhigiri")
cursor=conn.cursor()


@app.route("/")
def home():
	if 'userid' in session:
		ext="base1.html"
	else:
		ext="base.html"
	a=datetime.datetime.now()
	b=datetime.date.today()
	c=a.strftime("%H:%M:%S")	
	print(b)
	print(a) 
	print(c)
	return render_template("home1.html",ext=ext)


@app.route("/dashuser")
def dashuser():
	
	log=login.query.filter_by()
	return render_template("autable.html",log=log)


@app.route("/dashboard",methods=['GET','post'])
def dash1():
	username=request.form.get('username')
	password= request.form.get('password')
	cursor.execute("""SELECT * FROM `admin` WHERE `username` Like '{}' AND `password` Like '{}'""".format(username,password))
	user1=cursor.fetchall()
	if len(user1)>0:
		session['useri']=user1[0][0]
		if user1[0][4]=="museum":
			session['useri']=user1[0][0]
			return redirect("/dashmu")
		else:
			if 'useri' in session:

				return render_template("adminpanel.html")
			else:
				return render_template("adminlogin.html")
	else:
		if 'useri' in session:
			return render_template("adminpanel.html")
		else:
			return render_template("adminlogin.html")
		
@app.route("/dashproduct",methods=['GET','post'])
def dashproduct():
	products=product.query.all()
	cursor.execute("""SELECT category FROM `product`""")
	prod3=cursor.fetchall()
	
	res=[]
	for i in prod3:

		abc=i
		ced=(abc[0])
		if ced not in res:
			res.append(ced)
			# print([i][0])
			
	print(res)
	
	for j in res:
		cursor.execute("""SELECT * FROM `product` where category like '{}' """.format(j))
		prod4=cursor.fetchall()
		
		if len(prod4)>0:
			pass
		else:
			res.remove(j)
		


	if 'useri' in session:

		return render_template("aptable.html",prods=products,prod3=prod3,res=res)
	else:
		return redirect('/dashboard')

@app.route("/productinfo/<int:no>",methods=['GET','post'])
def productinfo(no):
	products=product.query.filter_by(productno=no)
	if 'useri' in session:

		return render_template("productinfo.html",prods=products)
	else:
		return redirect('/dashboard')

@app.route("/stock",methods=['GET','post'])
def stock1():
	cursor.execute("""SELECT name,pid FROM `product`""")
	products= cursor.fetchall()
	print(products)
	cursor.execute("""SELECT pid FROM `product`""")
	prid= cursor.fetchall()
	print(prid)
	cursor.execute("""SELECT pid,stock FROM `stock`""")
	stock= cursor.fetchall()
	print(stock)
	list1=[]
	for j in prid:
		print(j[0])
		jb=j[0]
		cursor.execute("""SELECT stock FROM `stock` where pid like '{}' """.format(jb))
		abc=cursor.fetchall()
		print(abc)
		if len(abc)>0:
			list2=[]
			a=(abc[::-1])
			b=(a[0][0])
			print(b)
			list2.append(j[0])
			list2.append(b)
			list1.append(list2)
	print("hi")
	print(list1)
	return render_template("stock.html",prod=products,list1=list1)


@app.route("/addstock/<int:no>",methods=['GET','post'])
def addstock(no):
	cursor.execute("""SELECT * FROM `product` WHERE pid Like '{}' """.format(no))
	products= cursor.fetchall()
	print(products)
	if 'useri' in session:

		return render_template("addstock.html",prods=products)
	else:
		return redirect('/dashboard')

@app.route("/addstock1/<int:no>",methods=['GET','post'])
def addstock1(no):
	date=datetime.date.today()
	abcdef=datetime.datetime.now()
	
	cdef=abcdef.strftime("%H:%M:%S")
	pid=no
	cursor.execute("""SELECT stock FROM `stock` WHERE pid Like '{}' """.format(no))
	products= cursor.fetchall()
	a=(products[::-1])
	b=(a[0][0])

	stocka=request.form.get('stock')
	nstock=int(b)+int(stocka)
	cursor.execute("""INSERT INTO `stock` VALUES(NULL,"{}","{}","{}","{}","{}","stock added")""".format(pid,nstock,stocka,date,cdef))
		
	conn.commit()
	return redirect('/stock')

@app.route("/removestock/<int:no>",methods=['GET','post'])
def removestock(no):
	cursor.execute("""SELECT * FROM `product` WHERE pid Like '{}' """.format(no))
	products= cursor.fetchall()
	print(products)
	cursor.execute("""SELECT stock FROM `stock` WHERE pid Like '{}' """.format(no))
	products1= cursor.fetchall()
	a=(products1[::-1])
	b=(a[0][0])
	if 'useri' in session:

		return render_template("removestock.html",prods=products,b=b)
	else:
		return redirect('/dashboard')	

@app.route("/removestock1/<int:no>",methods=['GET','post'])
def removestock1(no):
	date=datetime.date.today()
	abcdef=datetime.datetime.now()
	
	cdef=abcdef.strftime("%H:%M:%S")
	pid=no
	cursor.execute("""SELECT stock FROM `stock` WHERE pid Like '{}' """.format(no))
	products= cursor.fetchall()
	a=(products[::-1])
	b=(a[0][0])
	stocka=request.form.get('stock')
	nstock=int(b)-int(stocka)
	cursor.execute("""INSERT INTO `stock` VALUES(NULL,"{}","{}","{}","{}","{}","stock removed")""".format(pid,nstock,stocka,date,cdef))
		
	conn.commit()
	return redirect('/stock')

@app.route("/dorder",methods=['GET','POST'])
def dorder():
	cursor.execute("""SELECT `cid`,`productid`,`qty`,buying.amount,`date`,`time`,`paytype`,`type`,`name`,`village`,`tahsil`,`district`,`state`,address.phone,`pincode` from `buying`,`login`,`address`,`order_detail` where buying.custmerid=login.id and buying.addressid=address.addressid and delivery="not" and buying.orderid=order_detail.orderid """)
	order1=cursor.fetchall()
	cursor.execute("""SELECT `cid`,`productid`,`qty`,buying.amount,`date`,`time`,`paytype`,`type`,`username`,`village`,`tahsil`,`district`,`state`,address.phone,`pincode` from `buying`,`login`,`address`,`order_detail` where buying.custmerid=login.id and buying.addressid=address.addressid and delivery="yes" and buying.orderid=order_detail.orderid """)
	order2=cursor.fetchall()
	print(order1)
	return render_template("dorder.html",order=order1,order2=order2)	

@app.route("/dash",methods=['GET','post'])
def dash():
	username=request.form.get('username')
	password= request.form.get('password')
	print("username is")
	print(password)
	cursor.execute("""SELECT * FROM `admin` WHERE `username` Like '{}' AND `password` Like '{}'""".format(username,password))
	user1=cursor.fetchall()
	if len(user1)>0:
		session['useri']=user1[0][0]
	if 'useri' in session:

		return render_template("dash.html")
	else:
		return render_template("adminlogin.html")

@app.route("/dashsub" ,methods=['POST'])
def dashsub():
	if (request.method=='POST'):
		f=request.files['file1']
		# f=request.file['file1']
		f.save(os.path.join(app.config['upload_loc'],secure_filename(f.filename)))
	name= request.form.get('product_name')	 
	price= request.form.get('price')
	pid= request.form.get('pid')
	desc= request.form.get('desc')
	img= request.form.get('img')
	cat=request.form.get('category')
	stocka=request.form.get('stock')
	date=datetime.date.today()
	abcdef=datetime.datetime.now()
	
	cdef=abcdef.strftime("%H:%M:%S")
	cursor.execute("""SELECT * FROM `product` WHERE name Like '{}' """.format(name))
	users= cursor.fetchall()
	if len(users)>0:
		return redirect('/dashproduct')
	else:
			
		cursor.execute("""INSERT INTO `product` VALUES(NULL,"{}","{}","{}","{}","{}","{}")""".format(pid,name,price,desc,img,cat))
		cursor.execute("""INSERT INTO `stock` VALUES(NULL,"{}","{}","{}","{}","{}","initial added")""".format(pid,stocka,stocka,date,cdef))
		
		conn.commit()
		
		flash("added succefully")
		return redirect('/dashproduct')

@app.route("/dashsub1/<int:no>" ,methods=['GET','POST'])
def dashsub1(no):
	
	name= request.form.get('product_name')	 
	price= request.form.get('price')
	pid= request.form.get('pid')
	desc= request.form.get('desc')
	img= request.form.get('img')
	category=request.form.get('cat')
	products=product.query.filter_by(productno=no).first()
	products.name=name
	products.price=price
	products.pid=pid
	products.desci=desc
	products.img=img
	products.category=category
	db.session.commit()
	# cursor.execute("""UPDATE `product` SET name="{}",price="{}",desci="{}",img="{}" WHERE ids="{}")""".format(name,price,desc,img,no))
	# conn.commit()
	flash("update succefully")
	return redirect('/dashproduct')

@app.route("/dashsub2/<int:no>" ,methods=['GET','POST'])
def dashsub2(no):
	products=product.query.filter_by(productno=no).first()
	db.session.delete(products)
	db.session.commit()

	return redirect('/dashproduct')

@app.route("/login")
def login1():
	return render_template("log_in.html")

@app.route("/loginval" ,methods=['POST'])
def loginval():
	uusername= request.form.get('username')
	ppassword= request.form.get('password')
	print(uusername)
	print(ppassword)
	# cursor.execute("""SELECT * FROM `login` WHERE `username` Like '{}' AND `password` Like '{}'""".format(uusername,ppassword))
	# cursor.execute("""SELECT * FROM `login`""")

	cursor.execute("""SELECT * FROM `login` WHERE `password` Like '{}' """.format(ppassword))

	
	user1=cursor.fetchall()
	print(user1)
	
	if len(user1)>0:
		session['userid']=user1[0][0]

		return redirect('/')
	else:
		flash("invalid username or password")
		return render_template("log_in.html")	

@app.route("/register") 
def register():
	return render_template("register.html")

@app.route("/registerval" ,methods=['POST'])
def registerval():
	username= request.form.get('username')
	email= request.form.get('email')
	password= request.form.get('password')
	repass= request.form.get('repass')
	phone= request.form.get('phone')
	
	cursor.execute("""SELECT * FROM `login` WHERE username Like '{}' OR email Like'{}'""".format(username,email))
	users= cursor.fetchall()
	print(users)

	if users:
		if username==users[0][1] and email!=users[0][2]:
			flash("username already used")
			a=True
		else:
			flash("account already exist")
			a=True
	elif not  re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
		flash("use strong password")
		a=True
	elif password!=repass:
		flash("password not match")
		a=True
	elif len(phone)>10 or len(phone)<10:
		flash("enter valid phone no.")
		a=True
	else:
		a=False
	if a==True:
		#use redirect here ;
		return render_template("register.html")
	else :
		cursor.execute("""INSERT INTO `login` VALUES(NULL,"{}","{}","{}","{}")""".format(username,email,password,phone))
		conn.commit()
		return redirect('/login')




@app.route("/as")
def assa():
	if 'userid' in session:
		return render_template("as.html")
	else:
		return redirect('/')

@app.route("/about")
def about():
	if 'userid' in session:
		ext="base1.html"
	else:
		ext="base.html"
	return render_template("about.html",ext=ext)

@app.route("/museum")
def museum():
	if 'userid' in session:
		ext="base1.html"
	else:
		ext="base.html"
	
	return render_template("museum1.html",ext=ext)

@app.route("/booking",methods=['POST','GET'])
def booking():
	if 'userid' in session:
		ext="cmbase1.html"
	else:
		ext="cmbase.html" 
	cursor.execute("""SELECT bno FROM `nbooking`""")
	no=cursor.fetchall()
	a=(no[::-1])

	# print(a)
	
	b=(a[0][0])
	date=datetime.date.today()
	print(date)
	return render_template("booking.html",bno=b,ext=ext,date=date)

@app.route("/booking2",methods=['POST','GET'])
def booking2():
	if request.method=="POST":
		cursor.execute("""SELECT bno FROM `nbooking`""")
		no=cursor.fetchall()
		a=(no[::-1])

		b=(a[0][0])
		b=b+1
		name=request.form.get('name')
		phone=request.form.get('phone')
		add=request.form.get('add')
		adhar=request.form.get('adhar')
		normal=request.form.get('normal')
		kids=request.form.get('kids')
		print(kids)
		if normal=="":
			normal=0
		if kids=="":
			kids=0
		time=request.form.get('hours')
		date=request.form.get('date')
		normal=int(normal)
		kids=int(kids)
		cursor.execute("""INSERT INTO `nbooking` VALUES(NULL,"{}","{}","{}","{}","{}","{}","{}")""".format(date,name,phone,adhar,add,normal,kids))
		conn.commit()
		return render_template("pay.html",bno=b,name=name,adhar=adhar,normal=normal,kids=kids,time=time,date=date)


@app.route("/bookinge/<int:no>",methods=['POST','GET'])
def bookinge(no):
		
		name=request.form.get('name')
		phone=request.form.get('phone')
		add=request.form.get('add')
		adhar=request.form.get('adhar')
		normal=request.form.get('normal')
		kids=request.form.get('kids')
		if normal=="":
			normal=0
		if kids=="":
			kids=0
		date=request.form.get('date')

		nbookings=nbooking.query.filter_by(bno=no).first()
		nbookings.name=name
		nbookings.phone=phone
		nbookings.address=add
		nbookings.adhar=adhar
		nbookings.normal=normal
		nbookings.kids=kids
		
		nbookings.date=date
		db.session.commit()
		no=str(no)
		return redirect('/pay2/'+no)

@app.route("/pay2/<int:no>",methods=['POST','GET'])	
def pay2(no):
	nbooks1=nbooking.query.filter_by(bno=no)
	return render_template("pay2.html",nbooks=nbooks1)

@app.route("/pay3/<int:no>",methods=['POST','GET'])	
def pay3(no):
	nbookings=nbooking.query.filter_by(bno=no).first()
	db.session.delete(nbookings)
	db.session.commit()
	return redirect('/museum')



@app.route("/booking3/<int:no>",methods=['POST','GET'])
def booking3(no):
	nbooks=nbooking.query.filter_by(bno=no)
	date=datetime.date.today()
	print(date)
	return render_template("book3.html",nbooks=nbooks,date=date)

@app.route("/lpay/<int:no>",methods=['POST','GET'])
def lpay(no):
	print(no)
	cursor.execute("""SELECT * FROM `nbooking` WHERE `bno` Like '{}' """.format(no))
	lpay=cursor.fetchall()
	# lpay=nbooking.query.filter_by(bno=no)
	print(lpay)
	return render_template("lpay.html",lpays=lpay)

@app.route("/lpay2")
def lpay2():
	return render_template("lpay.html")


@app.route("/bookcard/<int:bno>/<int:adhar>",methods=['GET','POST'])
def bookcard(bno,adhar):
	print(bno)
	print(adhar)
	
	cardtype=request.form.get('pay')
	name=request.form.get("name")
	cno=request.form.get("cardno1")
	cvv=request.form.get("cvv")
	expm=request.form.get("expm")
	expy=request.form.get("expy")
	# print("name :",name)
	# print("cno :",cno)
	# print("cvv :",cvv)
	# print("expdate :",expm+"/"+expy)
	# print("expdate :",expy)
	# print("type :",cardtype)
	expdate=expm+"/"+expy
	cursor.execute("""SELECT * FROM `bookingcard` WHERE `adhar` Like '{}' and `cardtype` LIKE '{}' """.format(adhar,cardtype))
	cardb=cursor.fetchall()
	print(cardb)
	if len(cardb)>0:
		cursor.execute("""UPDATE `bookingcard` SET `name`='{}',`cardno`='{}',`expdate`='{}',`cvv`='{}',`bno`='{}' WHERE `adhar` Like '{}' and `cardtype` Like '{}' """.format(name,cno,expdate,cvv,bno,adhar,cardtype))
		conn.commit()
		cursor.execute("""SELECT `cardid` FROM `bookingcard` WHERE `adhar` Like '{}' and `cardtype` Like '{}' and `cardno` Like '{}' and `cvv` Like '{}' """.format(adhar,cardtype,cno,cvv))
		cardidb=cursor.fetchall()
		session['cardidb']=cardidb
	else:
		cursor.execute("""INSERT INTO `bookingcard` VALUES(NULL,"{}","{}","{}","{}","{}","{}","{}")""".format(bno,adhar,name,cno,expdate,cvv,cardtype))
		conn.commit()
		cursor.execute("""SELECT `cardid` FROM `bookingcard` WHERE `adhar` Like '{}' and `cardtype` Like '{}' and `cardno` Like '{}' and `cvv` Like '{}' """.format(adhar,cardtype,cno,cvv))
		cardidb=cursor.fetchall()
		session['cardidb']=cardidb
	

	return render_template("bend.html",bno=bno)

@app.route("/bookingtrue/<int:bno>" ,methods=['GET','POST'])
def bookingtrue(bno):
	cursor.execute("""SELECT * FROM `nbooking` WHERE `bno` Like '{}' """.format(bno))
	lpay=cursor.fetchall()
	print(lpay)
	total=(lpay[0][6])*130+(lpay[0][7])*70
	adhar=lpay[0][4]
	payno=session['cardidb']
	payno=payno[0][0]
	paytype="card"
	session['adhar']=adhar
	session['bookingno']=lpay[0][0]
	visited="not"
	print(total)
	date=datetime.date.today()
	a=datetime.datetime.now()
	
	c=a.strftime("%H:%M:%S")
	cursor.execute("""INSERT INTO `finalbooked` VALUES("{}","{}","{}","{}","{}","{}","{}","{}")""".format(bno,adhar,payno,paytype,total,date,c,visited))
	conn.commit()
	return redirect("/ticket")

@app.route("/ticket",methods=['POST','GET'])
def ticket():
	if 'adhar' in session:
		adhar=session['adhar']
		bookingno=session['bookingno']
		cursor.execute("""SELECT * FROM `nbooking` WHERE `adhar` Like '{}' and `bno` Like '{}' """.format(adhar,bookingno))
		lpay=cursor.fetchall()
		session.pop('adhar')
		return render_template("ticket.html",lpays=lpay)

	else:
		bno=request.form.get("bno")
		adhar=request.form.get("adhar")
		phone=request.form.get("phone")
		print(bno)
		print(adhar)
		print(phone)

		if bno=="":
			print("in bno")
			if adhar=="":
				print("in adhar")
				return redirect('/ticketsearch')
			else:
				print("in adhar else")
				cursor.execute("""SELECT `bno` FROM `finalbooked` WHERE adhar Like '{}' and visited Like "not" """.format(adhar))
				fpay=cursor.fetchall()
				print(fpay)
				if len(fpay)>0:
					print("in adhar else if")
					bno=fpay[0][0]
					cursor.execute("""SELECT * FROM `nbooking` WHERE `bno` Like '{}' """.format(bno))
					lpay=cursor.fetchall()
					return render_template("ticket.html",lpays=lpay)
				else:
					print("in adhar else else")
					return redirect('/ticketsearch')
		else:
			print("in bno else")
			cursor.execute("""SELECT `bno` FROM `finalbooked` WHERE bno Like '{}' and visited Like "not" """.format(bno))
			fpay=cursor.fetchall()
			print(fpay)
			if len(fpay)>0:
				print("in bno else if")
				bno=fpay[0][0]
				cursor.execute("""SELECT * FROM `nbooking` WHERE `bno` Like '{}' """.format(bno))
				lpay=cursor.fetchall()
				return render_template("ticket.html",lpays=lpay)
			else:
				print("in bno else else")
				return redirect('/ticketsearch')

				
@app.route('/dashmu')
def dashmu():
	if 'useri' in session:

		return render_template("dashmu.html")
	else:
		return render_template("adminlogin.html")

@app.route('/dashticket',methods=['POST','GET'])
def dashticket():
	bno=request.form.get('bno')
	cursor.execute("""SELECT * FROM `nbooking` WHERE `bno` Like '{}' """.format(bno))
	lpay=cursor.fetchall()
	return render_template("dashticket.html",lpays=lpay)

@app.route('/dashvisited/<int:bno>',methods=['POST','GET'])
def dashvisited(bno):
	cursor.execute("""UPDATE `finalbooked` SET `visited`="yes" WHERE `bno` Like '{}'  """.format(bno))
	conn.commit()
	return redirect("/dashmu")

@app.route('/dashnotvisited/<int:bno>',methods=['POST','GET'])
def dashnotvisited(bno):
	cursor.execute("""UPDATE `finalbooked` SET `visited`="not" WHERE `bno` Like '{}'  """.format(bno))
	conn.commit()
	return redirect("/dashmu")

	
	

	
	
	

		
	
	
@app.route("/ticketsearch")
def ticketsearch():
	if 'userid' in session:
		ext="base1.html"
	else:
		ext="base.html"
	
	
	return render_template("ticketsearch.html",ext=ext)

	
@app.route("/ayurvedic")
def ayurvedic():
	if 'userid' in session:
		ext="base1.html"
	else:
		ext="base.html"
	
	products=product.query.all()
	return render_template("ayurvedic.html",ext=ext,prods=products)

@app.route("/prod1/<int:no>")
def prod(no):
	if 'userid' in session:
		ext="base1.html"
	else:
		ext="base.html"
	prod1=product.query.filter_by(pid=no).first()
	return render_template("product.html",ext=ext,prod=prod1)

@app.route("/buy/<int:no>" ,methods=['GET','POST'])
def buy(no):
	if 'userid' in session: 
		session['prodid']=no         
		return render_template("buyingadd2.html")
		
	else:
		return redirect('/login')

@app.route("/buy1", methods=['GET','POST'])
def buy1():
	abcd=request.form.get("fav")
	aname=request.form.get("an")
	avillage=request.form.get("av")
	atahsil=request.form.get("at")
	adistrict=request.form.get("ad")
	astate=request.form.get("as")
	aphone=request.form.get("aphone")
	apin=request.form.get("apin")
	print(aname,avillage,atahsil,adistrict,astate,aphone,apin)
	print(abcd)
	cid=session['userid']
	print(cid)
	cursor.execute("""SELECT * FROM `address` WHERE `cid` Like '{}' and `name` Like '{}' and `tahsil` Like '{}' and `district` Like '{}' and `state` Like '{}' and `pincode` Like '{}'  """.format(cid,aname,atahsil,adistrict,astate,apin))
	addr1=cursor.fetchall()
	prodid=session['prodid']
	prod1=product.query.filter_by(pid=prodid).first()
	print(prod1)



	if len(addr1)>0:
		srno1=addr1[0][0]
		cursor.execute("""UPDATE `address` SET `name`='{}',`village`='{}',`tahsil`='{}',`phone`='{}' WHERE `cid` Like '{}' and `pincode` Like '{}' and `addressid` Like '{}' """.format(aname,avillage,atahsil,aphone,cid,apin,srno1))
		conn.commit()
		cursor.execute("""SELECT `addressid` FROM `address` WHERE `cid` Like '{}' and `name` Like '{}' and `tahsil` Like '{}' and `district` Like '{}' and `state` Like '{}' and `pincode` Like '{}'  """.format(cid,aname,atahsil,adistrict,astate,apin))
		addrid=cursor.fetchall()
		session['addrid']=addrid
		if abcd=="cod":
			return render_template("buyingcd.html")
		elif abcd=="card":
			return render_template("buyingcc2.html",prod=prod1)
	
		else:
			return render_template("buyingnb.html")
	else:
		cursor.execute("""INSERT INTO `address` VALUES(NULL,"{}","{}","{}","{}","{}","{}","{}","{}")""".format(cid,aname,avillage,atahsil,adistrict,astate,aphone,apin))
		conn.commit()
		cursor.execute("""SELECT `addressid` FROM `address` WHERE `cid` Like '{}' and `name` Like '{}' and `tahsil` Like '{}' and `district` Like '{}' and `state` Like '{}' and `pincode` Like '{}'  """.format(cid,aname,atahsil,adistrict,astate,apin))
		addrid=cursor.fetchall()
		session['addrid']=addrid
		if abcd=="cod":
			return render_template("buyingcd.html")
		elif abcd=="card":
			return render_template("buyingcc2.html",prod=prod1)
	
		else:
			return render_template("buyingnb.html")

@app.route("/buy2", methods=['GET','POST'])
def buy2():
	cid=session['userid']
	type1=request.form.get("pay")
	name=request.form.get("name")
	cno=request.form.get("cardno")
	cvv=request.form.get("cvv")
	expdate=request.form.get("expdate")
	cursor.execute("""SELECT * FROM `card` WHERE `cid` Like '{}' and `card_type` Like '{}' and `cardno` Like '{}' and `cvv` Like '{}' """.format(cid,type1,cno,cvv))
	cardd=cursor.fetchall()
	if len(cardd)>0:
		cursor.execute("""UPDATE `card` SET `name`='{}',`cardno`='{}',`expdate`='{}',`cvv`='{}' WHERE `cid` Like '{}' and `card_type` Like '{}' """.format(name,cno,expdate,cvv,cid,type1))
		conn.commit()
		cursor.execute("""SELECT `cardid` FROM `card` WHERE `cid` Like '{}' and `card_type` Like '{}' and `cardno` Like '{}' and `cvv` Like '{}' """.format(cid,type1,cno,cvv))
		cardid=cursor.fetchall()
		print(cardid)
		print(cid,type1,cno,cvv)
		session['cardid']=cardid
	else:
		cursor.execute("""INSERT INTO `card` VALUES(NULL,"{}","{}","{}","{}","{}","{}")""".format(cid,name,cno,expdate,cvv,type1))
		conn.commit()
		cursor.execute("""SELECT `cardid` FROM `card` WHERE `cid` Like '{}' and `card_type` Like '{}' and `cardno` Like '{}' and `cvv` Like '{}' """.format(cid,type1,cno,cvv))
		cardid=cursor.fetchall()
		print(cardid)
		session['cardid']=cardid
		print(cid,type1,cno,cvv)
	return render_template("buyingend.html")	

@app.route("/buyingpaid",methods=['GET','POST'])
def buyingpaid():
	cid=(session['userid'])
	pid=(session['prodid'])

	addrno=(session['addrid'])
	cardno=(session['cardid'])
	addrno=addrno[0][0]
	cardno=cardno[0][0]
	prod1=product.query.filter_by(pid=pid).first()
	total=prod1.price
	pids=prod1.pid
	payt="card"
	print(cid,pid,addrno,cardno,total)
	date=datetime.date.today()
	abcdef=datetime.datetime.now()
	
	cdef=abcdef.strftime("%H:%M:%S")
	cursor.execute("""SELECT `orderid` FROM `buying` """)
	newsp=cursor.fetchall()
	newabc=(newsp[::-1])
	
	newxyz=(newabc[0][0])
	newxyz=newxyz+1
	cursor.execute("""INSERT INTO `buying` VALUES("{}","{}","{}","{}","{}","{}","paid","{}","{}","not")""".format(newxyz,cid,addrno,cardno,payt,total,date,cdef))
	cursor.execute("""INSERT INTO `order_detail` VALUES("{}","{}","1","{}","{}")""".format(newxyz,pid,total,total))
	conn.commit()
	cursor.execute("""SELECT `stock` FROM `stock` WHERE `pid` Like '{}' """.format(pids))
	stok=cursor.fetchall()
	print(stok)
	a=(stok[::-1])
	print(a)
	b=(a[0][0])
	print(b)
	stocka=b-1
	date=datetime.date.today()
	abcdef=datetime.datetime.now()
	
	cdef=abcdef.strftime("%H:%M:%S")
	cursor.execute("""INSERT INTO `stock` VALUES(NULL,"{}","{}","1","{}","{}","customer purchase")""".format(pids,stocka,date,cdef))
	conn.commit()
	return redirect('yourorder')
	


@app.route("/cart/<int:no>" ,methods=['GET','POST'])
def cart123(no):
	if 'userid' in session:          
		
		
		prod2=product.query.filter_by(pid=no).first()
		pid=prod2.pid
		rate=prod2.price
		cid=(session['userid'])
		cursor.execute("""SELECT * FROM `cart` WHERE `cid` Like '{}' and `pid` Like '{}' """.format(cid,pid))
		cart1=cursor.fetchall()
		

		if len(cart1)>0:
			qty=cart1[0][3]
			qty+=1
			cursor.execute("""UPDATE `cart` SET `qty`='{}' WHERE `cid` Like '{}' and `pid` Like '{}' """.format(qty,cid,pid))
			conn.commit()
		else:
			cursor.execute("""INSERT INTO `cart` VALUES(NULL,"{}","{}",1,"{}")""".format(cid,pid,rate))
			conn.commit()
		
		
		return redirect('/cart2')
		
		
		
	else:
		return redirect('/login')

@app.route("/cart2" ,methods=['GET','POST'])
def cart2():
	if 'userid' in session:
		cid=(session['userid'])
		# cursor.execute("""SELECT  FROM `cart` WHERE `cid` Like '{}'""".format(cid))
		# cart2=cursor.fetchall()
		cursor.execute("""SELECT `name`,`qty`,`rate`,cart.cartid,`img`,product.pid FROM `product`,`cart` WHERE `cid` Like '{}' and cart.pid=product.pid """.format(cid))
		prod1=cursor.fetchall()
		# print(cart2)
		print(prod1)
		products=product.query.all()
		# prod1=product.query.all()
		# cart1=cart.query.all()
		# print(cart1)
		return render_template("newcart.html",prod1=prod1,cid=cid,prods=products)
	else:
		return redirect('/login')

@app.route("/carte/<int:cid>/<int:sr>")
def carte(cid,sr):
	
	carte1=cart.query.filter_by(cartid=sr).first()
	product12=product.query.filter_by(pid=carte1.pid).first()
	cursor.execute("""SELECT stock FROM `stock` WHERE pid Like '{}' """.format(carte1.pid))
	products1= cursor.fetchall()
	a=(products1[::-1])
	b=(a[0][0])
	return render_template("cartedit2.html",cart=carte1,prod=product12,b=b)

@app.route("/carter/<int:no>",methods=['GET','POST'])
def carter(no):
	qty=request.form.get('qty')
	
	cursor.execute("""UPDATE `cart` SET `qty`='{}' WHERE `cartid` Like '{}' """.format(qty,no))
	conn.commit()
	print("updateted as")
	# carter1=cart.query.filter_by(srno=no).first()
	# carter1.qty=qty
	# db.session.commit()
	return redirect('/cart2')

@app.route("/carted/<int:no>",methods=['GET','POST'])
def carted(no):
	
	cursor.execute("""DELETE FROM `cart`  WHERE `cartid` Like '{}' """.format(no))
	conn.commit()
	# carter1=cart.query.filter_by(srno=no).first()
	# carter1.qty=qty
	# db.session.commit()
	return redirect('/cart2')

@app.route("/cartp")
def cartp():
	if 'userid' in session:
		cid=(session['userid'])
		cursor.execute("""SELECT `name`,`qty`,`rate`,`cartid`,`img` FROM `product`,`cart` WHERE `cid` Like '{}' and cart.pid=product.pid """.format(cid))
		prod1=cursor.fetchall()
		return render_template("cartpay1.html",prod1=prod1,cid=cid)

@app.route("/cartp2",methods=['GET','POST'])
def cartp2():
	if 'userid' in session:
		cid=(session['userid'])
	cursor.execute("""SELECT `cartid` FROM `cart` WHERE `cid` Like '{}'""".format(cid))
	prod1=cursor.fetchall()
	list1=[]
	list2=[]
	list3=[]
	for i in prod1:
		list1.append(i[0])
	
	for j in list1:
		j=str(j)
		name="vehi"+j
		
		a=request.form.get(name)
		list2.append(a)
	
	for x in list2:
		if x!=None:
			list3.append(x)
			
	
	list4=[]
	list5=[]
	list6=[]
	for y in list3:
		cursor.execute("""SELECT `name`,`qty`,`rate`,`cartid` FROM `cart`,`product` WHERE `cartid` Like '{}' and cart.pid=product.pid """.format(y))
		prod1=cursor.fetchall()
		cursor.execute("""SELECT `qty`,`rate` FROM `cart` WHERE `cartid` Like '{}' """.format(y))
		prod2=cursor.fetchall()
		cursor.execute("""SELECT  `pid`,`qty` FROM `cart` WHERE `cartid` Like '{}' """.format(y))
		product3=cursor.fetchall()
		list5.append(prod2)
		list6.append(product3)
		
		list4.append(prod1)
	
	session['bpid']=list6
	
	
	total=0
	for z in list5:
		b=z[0][0]*z[0][1]
		total=total+b
	
	session['total']=total
	abcd=request.form.get("fav")
	
	
	if abcd=="cod":
		return render_template("cartpfcd.html",prod1=list4,total=total)
	elif abcd=="card":
		return render_template("paymentdetailsp.html",prod1=list4,total=total)
	
	else:
		return render_template("cartpfnb.html",prod1=list4,total=total)

@app.route("/cartend",methods=['GET','POST'])
def cartend():
	if 'userid' in session:
		cid=(session['userid'])
	type1=request.form.get("pay")
	name=request.form.get("name")
	cno=request.form.get("cardno")
	cvv=request.form.get("cvv")
	expdate=request.form.get("expdate")

	aname=request.form.get("an")
	avillage=request.form.get("av")
	atahsil=request.form.get("at")
	adistrict=request.form.get("ad")
	astate=request.form.get("as")
	aphone=request.form.get("aphone")
	apin=request.form.get("apin")
	print(aname,avillage,atahsil,adistrict,astate,aphone,apin)
	print(type1,name,cno,cvv,expdate)
	cursor.execute("""SELECT * FROM `card` WHERE `cid` Like '{}' and `card_type` Like '{}' and `cardno` Like '{}' and `cvv` Like '{}' """.format(cid,type1,cno,cvv))
	cardd=cursor.fetchall()
	if len(cardd)>0:
		cursor.execute("""UPDATE `card` SET `name`='{}',`cardno`='{}',`expdate`='{}',`cvv`='{}' WHERE `cid` Like '{}' and `card_type` Like '{}' """.format(name,cno,expdate,cvv,cid,type1))
		conn.commit()
		cursor.execute("""SELECT `cardid` FROM `card` WHERE `cid` Like '{}' and `card_type` Like '{}' and `cardno` Like '{}' and `cvv` Like '{}' """.format(cid,type1,cno,cvv))
		cardid=cursor.fetchall()
		session['cardid']=cardid
	else:
		cursor.execute("""INSERT INTO `card` VALUES(NULL,"{}","{}","{}","{}","{}","{}")""".format(cid,name,cno,expdate,cvv,type1))
		conn.commit()
		cursor.execute("""SELECT `cardid` FROM `card` WHERE `cid` Like '{}' and `card_type` Like '{}' and `cardno` Like '{}' and `cvv` Like '{}' """.format(cid,type1,cno,cvv))
		cardid=cursor.fetchall()
		session['cardid']=cardid
	cursor.execute("""SELECT * FROM `address` WHERE `cid` Like '{}' and `name` Like '{}' and `tahsil` Like '{}' and `district` Like '{}' and `state` Like '{}' and `pincode` Like '{}'  """.format(cid,aname,atahsil,adistrict,astate,apin))
	addr1=cursor.fetchall()
	if len(addr1)>0:
		srno1=addr1[0][0]
		cursor.execute("""UPDATE `address` SET `name`='{}',`village`='{}',`tahsil`='{}',`phone`='{}' WHERE `cid` Like '{}' and `pincode` Like '{}' and `addressid` Like '{}' """.format(aname,avillage,atahsil,aphone,cid,apin,srno1))
		conn.commit()
		cursor.execute("""SELECT `addressid` FROM `address` WHERE `cid` Like '{}' and `name` Like '{}' and `tahsil` Like '{}' and `district` Like '{}' and `state` Like '{}' and `pincode` Like '{}'  """.format(cid,aname,atahsil,adistrict,astate,apin))
		addrid=cursor.fetchall()
		session['addrid']=addrid
	else:
		cursor.execute("""INSERT INTO `address` VALUES(NULL,"{}","{}","{}","{}","{}","{}","{}","{}")""".format(cid,aname,avillage,atahsil,adistrict,astate,aphone,apin))
		conn.commit()
		cursor.execute("""SELECT `addressid` FROM `address` WHERE `cid` Like '{}' and `name` Like '{}' and `tahsil` Like '{}' and `district` Like '{}' and `state` Like '{}' and `pincode` Like '{}'  """.format(cid,aname,atahsil,adistrict,astate,apin))
		addrid=cursor.fetchall()
		session['addrid']=addrid

	xyz=(session['bpid'])
	print(xyz)
	return render_template("cend.html")

@app.route("/cartpaid",methods=['GET','POST'])
def cartpaid():
	cid=(session['userid'])
	pid=(session['bpid'])

	addrno=(session['addrid'])
	cardno=(session['cardid'])
	addrno=addrno[0][0]
	cardno=cardno[0][0]
	total=(session['total'])
	payt="card"
	print(cid,pid,addrno,cardno,total)
	date=datetime.date.today()
	abcdef=datetime.datetime.now()
	cursor.execute("""SELECT `pid`,`price` FROM `product` """)
	prodsp=cursor.fetchall()

	cdef=abcdef.strftime("%H:%M:%S")
	cursor.execute("""SELECT `orderid` FROM `buying` """)
	newsp=cursor.fetchall()
	newabc=(newsp[::-1])
	

	newxyz=(newabc[0][0])
	newxyz=newxyz+1
	cursor.execute("""INSERT INTO `buying` VALUES("{}","{}","{}","{}","{}","{}","paid","{}","{}","not")""".format(newxyz,cid,addrno,cardno,payt,total,date,cdef))
	conn.commit()
	for i in pid:
		print(i[0])
		print(i[0][0])
		totalsp=0
		for jm in prodsp:
			if i[0][0]==jm[0]:
				totalsp=i[0][1]*jm[1]
				cursor.execute("""INSERT INTO `order_detail` VALUES("{}","{}","{}","{}","{}")""".format(newxyz,i[0][0],i[0][1],jm[1],totalsp))
				conn.commit()
	print(pid)
	list10=[]
	date=datetime.date.today()
	abcdef=datetime.datetime.now()
	
	cdef=abcdef.strftime("%H:%M:%S")
	for j in pid:
		list10.append(j[0])
	print("hi",list10)
	for i in list10:
		print(i[0])
		cursor.execute("""SELECT `stock` FROM `stock` WHERE `pid` Like '{}' """.format(i[0]))
		stok=cursor.fetchall()
		
		a=(stok[::-1])
		print(a)
		b=(a[0][0])
		print(b)
		xyz=i[1]
		xy=i[0]
		nstock=b-xyz
		cursor.execute("""INSERT INTO `stock` VALUES(NULL,"{}","{}","{}","{}","{}","customer purchase")""".format(xy,nstock,xyz,date,cdef))
		print("ha")

		cursor.execute("""DELETE FROM `cart` where `pid` like '{}' and `cid` like '{}' and `qty` like '{}'  """.format(xy,cid,xyz))
		print("ha")
		conn.commit()

	return redirect('/yourorder')



@app.route("/feedback",methods=['GET','POST'])
def feedback():
	if 'userid' in session:
		ext="base1.html"
	else:
		ext="base.html"
	if request.method=="POST":

		name= request.form.get('name')	 
		email= request.form.get('email')
		msg= request.form.get('msg')
		
		cursor.execute("""INSERT INTO `feedback` VALUES(NULL,"{}","{}","{}")""".format(name,email,msg ))
		conn.commit()
		flash("sent succefully")
		return render_template("feedback.html",ext=ext)
	else:
		return render_template("feedback.html",ext=ext)



@app.route("/contact",methods=['GET','POST'])
def contact():
	if 'userid' in session:
		ext="base1.html"
	else:
		ext="base.html"
	if request.method=="POST":

		name= request.form.get('name')
		addr= request.form.get('addr')	 
		email= request.form.get('email')
		phone= request.form.get('phone')
		
		cursor.execute("""INSERT INTO `contact` VALUES(NULL,"{}","{}","{}","{}")""".format(name,addr,email,phone ))
		conn.commit()
		flash("sent succefully")
		return render_template("contact.html",ext=ext)
	else:
		return render_template("contact.html",ext=ext)

@app.route("/logout")
def logout():
	session.pop('userid')
	return redirect('/')

@app.route("/logout1")
def logout1():
	session.pop('useri')
	return redirect('/')

@app.route('/profile')
def profile():
	cid=session['userid']
	print(cid)
	cursor.execute("""SELECT * FROM `login` where id like '{}' """.format(cid))
	looks=cursor.fetchall()
	cursor.execute("""SELECT * FROM `address` where cid like '{}' """.format(cid))
	looks1=cursor.fetchall()
	
	return render_template("profile.html",looks=looks,looks1=looks1)

@app.route('/yourcart')
def yourcart():
	if 'userid' in session:
		cid=(session['userid'])
		# cursor.execute("""SELECT  FROM `cart` WHERE `cid` Like '{}'""".format(cid))
		# cart2=cursor.fetchall()
		cursor.execute("""SELECT `name`,`qty`,`rate`,`cartid`,`img` FROM `product`,`cart` WHERE `cid` Like '{}' and cart.pid=product.pid """.format(cid))
		prod1=cursor.fetchall()
		# print(cart2)
		print(prod1)
		# prod1=product.query.all()
		# cart1=cart.query.all()
		# print(cart1)
		return render_template("yourcart.html",prod1=prod1,cid=cid)
	else:
		return redirect('/login')

@app.route('/yourorder')
def yourorder():
	if 'userid' in session:
		cid=(session['userid'])
		print(cid)
		abc="not"
		cursor.execute("""SELECT `productid`,`qty` FROM `buying`,`order_detail` WHERE `custmerid` Like '{}' and `delivery` Like '{}' and buying.orderid=order_detail.orderid  """.format(cid,abc))
		prod1=cursor.fetchall()
		print(prod1)
		cursor.execute("""SELECT `name`,`qty`,`price` FROM `product`,`buying`,`order_detail` WHERE `custmerid` Like '{}' and order_detail.productid=product.pid and buying.orderid=order_detail.orderid and `delivery` Like '{}' """.format(cid,abc))
		prod2=cursor.fetchall()
		print(prod2)
		
		return render_template("yourorder.html",prod2=prod2)
	else:
		return redirect('/login')	

@app.route("/admin_report")
def admin_report():
	if 'useri' in session:
		return render_template("report.html")

@app.route('/repo/allprod',methods=['GET','POST'])
def download_report():
	
	cursor.execute("""SELECT `pid`,`name`,`price` FROM `product` order by `name` asc""")
	result=cursor.fetchall()
	print(result)
	cursor.execute("""SELECT pid FROM `product`""")
	prid= cursor.fetchall()
	print(prid)
	list1=[]
	for j in prid:
		print(j[0])
		jb=j[0]
		cursor.execute("""SELECT stock FROM `stock` where pid like '{}' """.format(jb))
		abc=cursor.fetchall()
		print(abc)
		if len(abc)>0:
			list2=[]
			a=(abc[::-1])
			b=(a[0][0])
			print(b)
			list2.append(j[0])
			list2.append(b)
			list1.append(list2)
	print("hi")
	print(list1)

	pdf = FPDF()
	pdf.add_page()
		
	page_width = pdf.w - 2 * pdf.l_margin
		
	pdf.set_font('Times','B',30.0) 
	pdf.image('C:/Users/HP/myproject/venv/static/img/logo4.png',20,4,40,0,'PNG')
	pdf.cell(page_width, 0.0, 'Siddhigiri Math', align='C')
	pdf.ln(8)
	pdf.set_font('Times','B',14.0)
	pdf.cell(page_width, 0.0, 'Address:-Kaneri,tal-Karveer', align='C')
	pdf.ln(5)
	pdf.cell(page_width, 0.0, 'dist-Kolhapur,416234', align='C')
	pdf.ln(20)
	pdf.dashed_line(10, 30, 210, 30, 1, 10)
	pdf.set_font('Times','B',20.0)
	pdf.cell(page_width, 0.0, 'Product details', align='C')
	pdf.set_font('Times','B',14.0)
	pdf.ln(10)
	date=datetime.date.today()
	pdf.cell(page_width, 0.0, 'Date:-'+str(date.strftime("%d / %m / %y")),align='L')
	pdf.ln(10)
	pdf.cell(page_width, 0.0, 'The stock details on date '+str(date.strftime("%d / %m / %y")), align='C')
	pdf.set_font('Courier', '', 12)
	pdf.ln(10)	
	col_width = page_width/4
		
	pdf.ln(1)
		
	th = pdf.font_size
	pdf.set_text_color(r=87, g=0, b=0)
	
	pdf.cell(col_width*0.5,th,"Sr.No",border=1,align='C')
	pdf.cell(col_width,th,"Product name",border=1,align='C')
	pdf.cell(col_width,th,"Rate",border=1,align='C')
	pdf.cell(col_width,th,"Stock",border=1,align='C')
	pdf.ln(th)
	i=1
	pdf.set_text_color(r=0, g=0, b=0)
	
	for row in result:
		pdf.cell(col_width*0.5, th, str(i), border=1,align='C')
		pdf.cell(col_width, th, row[1], border=1,align='C')
		pdf.cell(col_width, th, str(row[2]), border=1,align='C')
		for stk in list1:
			if row[0]==stk[0]:
				pdf.cell(col_width, th,str(stk[1]), border=1,align='C')
		pdf.ln(th)
		i=i+1
		print(row)
		
	pdf.ln(10)
		
	pdf.set_font('Times','',10.0) 
	pdf.cell(page_width, 0.0, '- end of report -', align='C')
		
	return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=product-all_report.pdf'})

@app.route('/repo/particularprod')
def repo1():
	cursor.execute("""SELECT `name` FROM `product` """)
	data = cursor.fetchall()
	return render_template('indextest2.html',data=data)

@app.route('/repo/particularprod/down',methods=['GET','POST'])
def download_report1():
	if request.method == 'POST':
		
		name=request.form.get("name")
		# cursor = mysql.connection.cursor()
		
		# cursor.execute("""SELECT * FROM `login` WHERE Id BETWEEN '{}' AND '{}'  """.format(text,text1))
		# result=cursor.fetchall()
		cursor.execute("""SELECT `pid`,`name`,`price`,`desci` FROM `product` WHERE name Like '{}' """.format(name))
		result=cursor.fetchall()
		print(result)
		pid1=result[0][0]
		
		cursor.execute("""SELECT stock FROM `stock` where pid like '{}' """.format(pid1))
		abc=cursor.fetchall()
		print(abc)
		if len(abc)>0:
				
			a=(abc[::-1])
			b=(a[0][0])
				
			print(a)
			print(b)

		pdf = FPDF()
		pdf.add_page()
		
		page_width = pdf.w - 2 * pdf.l_margin
		
		pdf.set_font('Times','B',30.0) 
		pdf.image('C:/Users/HP/myproject/venv/static/img/logo4.png',20,4,40,0,'PNG')
		pdf.cell(page_width, 0.0, 'Siddhigiri Math', align='C')
		pdf.ln(8)
		pdf.set_font('Times','B',14.0)
		pdf.cell(page_width, 0.0, 'Address:-Kaneri,tal-Karveer', align='C')
		pdf.ln(5)
		pdf.cell(page_width, 0.0, 'dist-Kolhapur,416234', align='C')
		pdf.ln(20)
		pdf.dashed_line(10, 30, 210, 30, 1, 10)
		pdf.set_font('Times','B',14.0)
		pdf.cell(page_width, 0.0, 'Product details Of '+str(result[0][1]), align='C')
		pdf.ln(10)
		date=datetime.date.today()
		pdf.cell(page_width, 0.0, 'Date:-'+str(date.strftime("%d / %m / %y")),align='L')
		pdf.ln(10)
		pdf.set_font('Courier', '', 14)
		pdf.cell(page_width, 0.0, 'Product name:- '+str(result[0][1]),align='L')
		pdf.ln(7)
		# pdf.cell(page_width, 0.0, 'product Desription:- '+str(result[0][3]),encode('utf-8').decode('latin-1'),align='justify')
		# pdf.ln(7)
		pdf.cell(page_width, 0.0, 'Rate:- '+str(result[0][2]),align='L')
		pdf.ln(7)
		pdf.cell(page_width, 0.0, 'Stock:- '+str(b),align='L')
		pdf.ln(7)
		
		
		
		
		pdf.set_font('Times','',10.0) 
		pdf.cell(page_width, 0.0, '- end of report -', align='C')
		
		return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=partiproduct_report.pdf'})

@app.route('/repo/productdate')
def repo2():
	
	return render_template('productdate.html')

@app.route('/repo/productdate/down',methods=['GET','POST'])
def download_report2():
	if request.method == 'POST':
		
		intial=request.form.get("intial")
		final=request.form.get("final")

		
		cursor.execute("""SELECT `productid`,order_detail.qty,`date`,`time` FROM `buying`,`order_detail` WHERE date between '{}' and '{}' """.format(intial,final))
		result=cursor.fetchall()
		# print(result)
		cursor.execute("""SELECT `pid`,`name`,`price` FROM `product` """)
		result1=cursor.fetchall()
		print(result1)
		list1=[]
		for i in result1:
			list2=[]
			abc=i[0]
			cursor.execute("""SELECT sum(qty) FROM `buying`,`order_detail` where productid like '{}' and buying.orderid=order_detail.orderid """.format(abc))
			result2=cursor.fetchall()
			print(result2)
			list2.append(i[0])
			if result2[0][0]!=None:
				list2.append(result2[0][0])
			else:
				list2.append(0)

			list1.append(list2)		
		pdf = FPDF()
		pdf.add_page()
		
		page_width = pdf.w - 2 * pdf.l_margin
		
		pdf.set_font('Times','B',30.0) 
		pdf.image('C:/Users/HP/myproject/venv/static/img/logo4.png',20,4,40,0,'PNG')
		pdf.cell(page_width, 0.0, 'Siddhigiri Math', align='C')
		pdf.ln(8)
		pdf.set_font('Times','B',14.0)
		pdf.cell(page_width, 0.0, 'Address:-Kaneri,tal-Karveer', align='C')
		pdf.ln(5)
		pdf.cell(page_width, 0.0, 'dist-Kolhapur,416234', align='C')
		pdf.ln(20)
		pdf.dashed_line(10, 30, 210, 30, 1, 10)
		pdf.set_font('Times','B',14.0)
		pdf.cell(page_width, 0.0, 'Product Sold details', align='C')
		pdf.ln(10)
		date=datetime.date.today()
		pdf.cell(page_width, 0.0, 'Date:-'+str(date.strftime("%d / %m / %y")),align='L')
		pdf.ln(10)
		pdf.cell(page_width, 0.0, 'The Details are from date : '+intial+'   TO date : '+final, align='C')
		pdf.ln(10)
		pdf.set_font('Courier', '', 12)

		col_width = page_width/4
		
		pdf.ln(1)
		
		th = pdf.font_size
		pdf.set_text_color(r=87, g=0, b=0)
		pdf.cell(col_width*0.5,th,"Sr.No",border=1,align='C')
		pdf.cell(col_width,th,"Name",border=1,align='C')
		pdf.cell(col_width,th,"Quantity",border=1,align='C')
		pdf.cell(col_width,th,"Total(Rs)",border=1,align='C')
		pdf.ln(th)
		i=1
		print(list1)
		pdf.set_text_color(r=0, g=0, b=0)
		amount=0
		for row in result1:
			total=0
			pdf.cell(col_width*0.5, th, str(i), border=1,align='C')
			pdf.cell(col_width, th, row[1], border=1,align='C')
			for j in list1:
				if row[0]==j[0]:
					if j[1]=="None":
						total=0
					else:
						pdf.cell(col_width, th, str(j[1]), border=1,align='C')
						total=int(j[1])*int(row[2])
			pdf.cell(col_width, th, str(total)+".00", border=1,align='C')
			amount=amount+total
			pdf.ln(th)
			# print(row)
			i=i+1
		pdf.cell(col_width*3.5,th,"Total:-"+str(amount)+".00",border=1,align='R')
		pdf.ln(10)
		
		
		
		
		pdf.set_font('Times','',10.0) 
		pdf.cell(page_width, 0.0, '- end of report -', align='C')
		
		return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=product-datewise_report.pdf'})
			
@app.route('/repo/visitorsall',methods=['GET','POST'])
def download_report3():
	

		
	cursor.execute("""SELECT * FROM `finalbooked`,`nbooking` Where nbooking.bno=finalbooked.bno""")
	result=cursor.fetchall()
	print(result)
		
	pdf = FPDF()
	pdf.add_page()
		
	page_width = pdf.w - 2 * pdf.l_margin
		
	pdf.set_font('Times','B',30.0) 
	pdf.image('C:/Users/HP/myproject/venv/static/img/logo4.png',20,4,40,0,'PNG')
	pdf.cell(page_width, 0.0, 'Siddhigiri Math', align='C')
	pdf.ln(8)
	pdf.set_font('Times','B',14.0)
	pdf.cell(page_width, 0.0, 'Address:-Kaneri,tal-Karveer', align='C')
	pdf.ln(5)
	pdf.cell(page_width, 0.0, 'dist-Kolhapur,416234', align='C')
	pdf.ln(20)
	pdf.dashed_line(10, 30, 210, 30, 1, 10)
	pdf.set_font('Times','B',14.0)
	pdf.cell(page_width, 0.0, ' All Visitors details', align='C')
	pdf.ln(10)
	date=datetime.date.today()
	pdf.cell(page_width, 0.0, 'Date:-'+str(date.strftime("%d / %m / %y")),align='L')
	pdf.ln(10)
	pdf.cell(page_width, 0.0, 'The Details are from date : 03 / 01 / 22   TO date : '+str(date.strftime("%d / %m / %y")), align='C')
	pdf.ln(10)
	pdf.set_font('Courier', '', 12)

	col_width = page_width/6
		
	pdf.ln(1)
		
	th = pdf.font_size
	pdf.set_text_color(r=87, g=0, b=0)
	pdf.cell(col_width*0.5,th,"Sr.No",border=1,align='C')
	pdf.cell(col_width,th,"Booking no",border=1,align='C')
	pdf.cell(col_width*1.6,th,"Name",border=1,align='C')
		
	
	pdf.cell(col_width,th,"Adult",border=1,align='C')
	pdf.cell(col_width,th,"Kids",border=1,align='C')
	pdf.cell(col_width,th,"Amount(Rs)",border=1,align='C')
	pdf.ln(th)
	i=1
	pdf.set_text_color(r=0, g=0, b=0)
	for row in result:
		pdf.cell(col_width*0.5, th, str(i), border=1,align='C')
		pdf.cell(col_width, th, str(row[0]), border=1,align='C')
		pdf.cell(col_width*1.6, th, str(row[10]), border=1,align='C')
		
		pdf.cell(col_width, th, str(row[14]), border=1,align='C')
		pdf.cell(col_width, th, str(row[15]), border=1,align='C')
		pdf.cell(col_width, th, str(row[4])+".00 ", border=1,align='C')
		pdf.ln(th)
			
		i=i+1
		
		
		
			
		
	pdf.ln(10)
		
		
		
		
	pdf.set_font('Times','',10.0) 
	pdf.cell(page_width, 0.0, '- end of report -', align='C')
		
	return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=visitor-all.pdf'})

@app.route('/repo/visitoradult')
def repo4():
	
	return render_template('visitoradult.html')

@app.route('/repo/visitoradult/down',methods=['GET','POST'])
def download_report4():
	if request.method == 'POST':
		
		intial=request.form.get("intial")
		final=request.form.get("final")

		
		cursor.execute("""SELECT sum(normal) FROM `finalbooked`,`nbooking` Where nbooking.bno=finalbooked.bno and finalbooked.date between '{}' and '{}' """.format(intial,final))
		result=cursor.fetchall()
		print(result[0][0])
		abc=result[0][0]
		print(abc)
		if abc!=None:
			abc=int(abc)
		else:
			abc=0
		pdf = FPDF()
		pdf.add_page()
		
		page_width = pdf.w - 2 * pdf.l_margin
		
		pdf.set_font('Times','B',30.0) 
		pdf.image('C:/Users/HP/myproject/venv/static/img/logo4.png',20,4,40,0,'PNG')
		pdf.cell(page_width, 0.0, 'Siddhigiri Math', align='C')
		pdf.ln(8)
		pdf.set_font('Times','B',14.0)
		pdf.cell(page_width, 0.0, 'Address:-Kaneri,tal-Karveer', align='C')
		pdf.ln(5)
		pdf.cell(page_width, 0.0, 'dist-Kolhapur,416234', align='C')
		pdf.ln(20)
		pdf.dashed_line(10, 30, 210, 30, 1, 10)
		pdf.set_font('Times','B',14.0)
		pdf.cell(page_width, 0.0, 'Visitors details for Adult', align='C')
		pdf.ln(10)
		date=datetime.date.today()
		pdf.cell(page_width, 0.0, 'Date:-'+str(date.strftime("%d / %m / %y")),align='L')
		pdf.ln(10)
		pdf.set_font('Courier', '', 14)

		pdf.cell(page_width, 0.0, 'from Date:- '+intial, align='l')
		pdf.ln(10)
		pdf.cell(page_width, 0.0, 'to Date:- '+final, align='l')
		pdf.ln(10)
		pdf.cell(page_width, 0.0, 'Total visited Adults :- '+str(abc), align='l')
		pdf.ln(10)
		
		
		
		
			
		
		pdf.ln(10)
		
		
		
		
		pdf.set_font('Times','',10.0) 
		pdf.cell(page_width, 0.0, '- end of report -', align='C')
		
		return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=visitor-adult.pdf'})
	
@app.route('/repo/visitorkids')
def repo5():
	
	return render_template('visitorkids.html')

@app.route('/repo/visitorkids/down',methods=['GET','POST'])
def download_report5():
	if request.method == 'POST':
		
		intial=request.form.get("intial")
		final=request.form.get("final")

		
		cursor.execute("""SELECT sum(kids) FROM `finalbooked`,`nbooking` Where nbooking.bno=finalbooked.bno and finalbooked.date between '{}' and '{}' """.format(intial,final))
		result=cursor.fetchall()
		print(result[0][0])
		abc=result[0][0]
		print(abc)
		if abc !=None:
			abc=int(abc)
		else:
			abc=0
		pdf = FPDF()
		pdf.add_page()
		
		page_width = pdf.w - 2 * pdf.l_margin
		
		pdf.set_font('Times','B',30.0) 
		pdf.image('C:/Users/HP/myproject/venv/static/img/logo4.png',20,4,40,0,'PNG')
		pdf.cell(page_width, 0.0, 'Siddhigiri Math', align='C')
		pdf.ln(8)
		pdf.set_font('Times','B',14.0)
		pdf.cell(page_width, 0.0, 'Address:-Kaneri,tal-Karveer', align='C')
		pdf.ln(5)
		pdf.cell(page_width, 0.0, 'dist-Kolhapur,416234', align='C')
		pdf.ln(20)
		pdf.dashed_line(10, 30, 210, 30, 1, 10)
		pdf.set_font('Times','B',14.0)
		pdf.cell(page_width, 0.0, 'Visitors details for kids', align='C')
		pdf.ln(10)
		date=datetime.date.today()
		pdf.cell(page_width, 0.0, 'Date:-'+str(date.strftime("%d / %m / %y")),align='L')
		pdf.ln(10)
		pdf.set_font('Courier', '', 14)

		pdf.cell(page_width, 0.0, 'from Date:- '+intial, align='l')
		pdf.ln(10)
		pdf.cell(page_width, 0.0, 'to Date:- '+final, align='l')
		pdf.ln(10)
		pdf.cell(page_width, 0.0, 'Total visited kids :- '+str(abc), align='l')
		pdf.ln(10)
		
		
		
		
			
		
		pdf.ln(10)
		
		
		
		
		pdf.set_font('Times','',10.0) 
		pdf.cell(page_width, 0.0, '- end of report -', align='C')
		
		return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=visitor-kids.pdf'})
	
@app.route('/repo/visitordate')
def repo6():
	
	return render_template('visitordate.html')

@app.route('/repo/visitordate/down',methods=['GET','POST'])
def download_report6():
	if request.method == 'POST':
		
		intial=request.form.get("intial")
		final=request.form.get("final")

		
		cursor.execute("""SELECT * FROM `finalbooked`,`nbooking` Where nbooking.bno=finalbooked.bno and finalbooked.date between '{}' and '{}' """.format(intial,final))
		result=cursor.fetchall()
		print(result)
		
		pdf = FPDF()
		pdf.add_page()
		
		page_width = pdf.w - 2 * pdf.l_margin
		
		pdf.set_font('Times','B',30.0) 
		pdf.image('C:/Users/HP/myproject/venv/static/img/logo4.png',20,4,40,0,'PNG')
		pdf.cell(page_width, 0.0, 'Siddhigiri Math', align='C')
		pdf.ln(8)
		pdf.set_font('Times','B',14.0)
		pdf.cell(page_width, 0.0, 'Address:-Kaneri,tal-Karveer', align='C')
		pdf.ln(5)
		pdf.cell(page_width, 0.0, 'dist-Kolhapur,416234', align='C')
		pdf.ln(20)
		pdf.dashed_line(10, 30, 210, 30, 1, 10)
		pdf.set_font('Times','B',14.0)
		pdf.cell(page_width, 0.0, 'Visitors details ', align='C')
		pdf.ln(10)
		date=datetime.date.today()
		pdf.cell(page_width, 0.0, 'Date:-'+str(date.strftime("%d / %m / %y")),align='L')
		pdf.ln(10)
		pdf.cell(page_width, 0.0, 'The Details are from date : '+intial+'   TO date : '+final, align='C')
		pdf.ln(10)
		pdf.set_font('Courier', '', 12)

		col_width = page_width/6
		
		pdf.ln(1)
		
		th = pdf.font_size
		pdf.set_text_color(r=87, g=0, b=0)
		pdf.cell(col_width*0.5,th,"Sr.No",border=1,align='C')
		pdf.cell(col_width,th,"Booking no",border=1,align='C')
		pdf.cell(col_width*1.5,th,"Name",border=1,align='C')
		
		
		pdf.cell(col_width,th,"Adult",border=1,align='C')
		pdf.cell(col_width,th,"Kids",border=1,align='C')
		pdf.cell(col_width,th,"Amount(Rs)",border=1,align='C')
		pdf.ln(th)
		i=1
		pdf.set_text_color(r=0, g=0, b=0)
		for row in result:
			pdf.cell(col_width*0.5, th, str(i), border=1,align='C')
			pdf.cell(col_width, th, str(row[0]), border=1,align='C')
			pdf.cell(col_width*1.5, th, str(row[10]), border=1,align='C')
			
			pdf.cell(col_width, th, str(row[14]), border=1,align='C')
			pdf.cell(col_width, th, str(row[15]), border=1,align='C')
			pdf.cell(col_width, th, str(row[4])+".00 ", border=1,align='C')
			pdf.ln(th)
			
			i=i+1
		
		
		
			
		
		pdf.ln(10)
		
		
		
		
		pdf.set_font('Times','',10.0) 
		pdf.cell(page_width, 0.0, '- end of report -', align='C')
		
		return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=visitor-datewise.pdf'})

@app.route('/repo/customer')
def repo7():
	cursor.execute("""SELECT `username`,`id` FROM `login` """)
	data = cursor.fetchall()
	return render_template('indextest3.html',data=data)		
					
@app.route('/repo/custmer/down',methods=['GET','POST'])
def download_report7():
	if request.method == 'POST':
		
		name=request.form.get("name")
		cursor.execute("""SELECT * FROM `login` WHERE username Like '{}' """.format(name))
		num1=cursor.fetchall()
		no=num1[0][0]
		cursor.execute("""SELECT * FROM `login` WHERE id Like '{}' """.format(no))
		log=cursor.fetchall()
		cursor.execute("""SELECT buying.date,product.name,order_detail.qty,product.price,buying.delivery FROM `product`,`order_detail`,`buying` WHERE buying.custmerid Like '{}' and order_detail.orderid=buying.orderid and order_detail.productid=product.pid """.format(no,))
		result=cursor.fetchall()
		print(result)
		
		
		

		pdf = FPDF()
		pdf.add_page()
		
		page_width = pdf.w - 2 * pdf.l_margin
		
		pdf.set_font('Times','B',30.0) 
		pdf.image('C:/Users/HP/myproject/venv/static/img/logo4.png',20,4,40,0,'PNG')
		pdf.cell(page_width, 0.0, 'Siddhigiri Math', align='C')
		pdf.ln(8)
		pdf.set_font('Times','B',14.0)
		pdf.cell(page_width, 0.0, 'Address:-Kaneri,tal-Karveer', align='C')
		pdf.ln(5)
		pdf.cell(page_width, 0.0, 'dist-Kolhapur,416234', align='C')
		pdf.ln(20)
		pdf.dashed_line(10, 30, 210, 30, 1, 10)
		pdf.set_font('Times','B',14.0)
		pdf.cell(page_width, 0.0, 'Customer Details', align='C')
		pdf.ln(10)
		date=datetime.date.today()
		pdf.cell(page_width, 0.0, 'Date:-'+str(date.strftime("%d / %m / %y")),align='L')
		pdf.ln(10)
		pdf.set_font('Courier', '', 14)
		pdf.cell(page_width, 0.0, 'Customer Id :- '+str(log[0][0]),align='L')
		pdf.ln(8)
		
		pdf.cell(page_width, 0.0, 'Customer Name :- '+str(log[0][1]),align='L')
		pdf.ln(8)
		pdf.cell(page_width, 0.0, 'Customer Email :- '+str(log[0][2]),align='L')
		pdf.ln(8)
		pdf.set_font('Courier', '', 12)
		col_width = page_width/7
		
		pdf.ln(1)
		
		th = pdf.font_size
		pdf.set_text_color(r=87, g=0, b=0)
		pdf.cell(col_width*0.5,th,"Sr.No",border=1,align='C')
		pdf.cell(col_width,th,"order Date",border=1,align='C')
		pdf.cell(col_width*1.5,th,"name",border=1,align='C')
		
		pdf.cell(col_width,th,"quntity",border=1,align='C')
		pdf.cell(col_width,th,"Rate(Rs)",border=1,align='C')
		pdf.cell(col_width,th,"Price(Rs)",border=1,align='C')
		pdf.cell(col_width,th,"Delivery",border=1,align='C')
		pdf.ln(th)
		i=1
		pdf.set_text_color(r=0, g=0, b=0)
		for row in result:
			pdf.cell(col_width*0.5, th, str(i), border=1,align='C')
			pdf.cell(col_width, th, str(row[0]), border=1,align='C')
			pdf.cell(col_width*1.5, th, str(row[1]), border=1,align='C')
			pdf.cell(col_width, th, str(row[2]), border=1,align='C')
			pdf.cell(col_width, th, str(row[3])+"0 ", border=1,align='C')
			a=row[2]*row[3]
			pdf.cell(col_width, th, str(a)+"0 ", border=1,align='C')
			pdf.cell(col_width, th, str(row[4]), border=1,align='C')
			pdf.ln(th)
			
			i=i+1
		
		
		
			
		
		pdf.ln(10)
		
		
		
		
		
		
		
		pdf.set_font('Times','',10.0) 
		pdf.cell(page_width, 0.0, '- end of report -', align='C')
		
		return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=customer_details.pdf'})


if __name__ == '__main__':
	app.run(debug=True)