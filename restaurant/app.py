from flask import Flask,render_template,url_for,request, redirect, flash
app=Flask(__name__)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant


engine = create_engine("sqlite:///restaurantmenu.db",connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
datas=[
	{
	   'id':1,
	   'title':'Python CodeBlock',
	   'author': 'GidoVan Rosum',
	   'description':'This is the Python Book...!'
	},
	{
	   'id':2,
	   'title':'Angular Complete',
	   'author': 'Google',
	   'description':'This is the Angular Book...!'
	}
]

@app.route("/")
@app.route("/home")
def home():
	return render_template("home.html")

@app.route('/addrestaurant')
def Addrestaurant():
	return render_template('addrestaurant.html')

@app.route('/new_restaurant',methods=['GET','POST'])
def newRestaurant():
	if request.method == "POST":
		name=request.form['rname']
		addRest = Restaurant(name=name)
		session.add(addRest)
		session.commit()
		flash('New Restaurant added Successfully...!','success')
		return redirect('/restaurants')
	else:
		return render_template('addrestaurant.html')
	return render_template('addrestaurant.html')



@app.route('/edit/<int:rest_id>',methods=["GET","POST"])
def editRestaurant(rest_id):
	if request.method == "POST":
		name = request.form['rname']

		getId = session.query(Restaurant).filter_by(id=rest_id).one()
		getId.name = name
		
		session.commit()
		flash('Restaurant Updated Successfully...!','info')
		return redirect('/restaurants')
	
	else:
		getId = session.query(Restaurant).filter_by(id=rest_id).one()
		return render_template("editRestaurant.html",myRests = getId)
	return render_template("editRestaurant.html")

@app.route('/delete/<int:rest_id>',methods=["GET"])
def deleteRestaurant(rest_id):
	getId = session.query(Restaurant).filter_by(id=rest_id)
	getId.delete()
	session.commit()
	flash('Restaurant Deleted Successfully...!','warning')
	return redirect("/restaurants")


@app.route('/restaurants')
def showRestaurants():
	rests = session.query(Restaurant).all() 
	return render_template('restaurants.html',restaurants=rests)

if __name__ == '__main__':
	app.config['SECRET_KEY'] = '3467dc5a882760e8016934e583a93bed99b55d91'
	app.debug=True
	app.run(host="0.0.0.0",port=5000)