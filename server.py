from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Project, Wall, Wall_Art, Artwork, connect_to_db, db 

app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined




@app.route('/')
def index():
    """Homepage."""
  
    return render_template("homepage.html")


@app.route('/wallforms')
def gather_wall_info():
    """Gather wall information"""

    return render_template("wall_forms.html")


@app.route('/artforms')
def gather_art_info():
    """Gather artwork information"""

    return render_template("art_forms.html")




##################################
  #Calc_display/ Calculations
##################################


@app.route('/calcdisplay')
def calcs():
    """Graphic Display of Calculations"""

    return render_template("calc_display.html")




@app.route('/calculations')
def plain_calcs():
    """Text only display of calculations"""

    return render_template("calculations.html")





##################################
	#SIGN UP/ LOGIN/ SIGN OUT 
##################################


@app.route("/register")
def user_signup():
    """Sign up a new user."""

    return render_template("/register.html")

#add jinja forms!
@app.route("/register-process", methods=['POST'])
def process_signup():
    """Route to process login for users."""

    entered_email = request.form['email']
    entered_username = request.form['user_name']
    entered_pw = request.form['password']
    entered_pw2 = request.form['password2']
    
    user = User.query.filter_by(email=entered_email).first()

    if request.method == "POST":
        if user == None: # is not in User Table?
            print user 
            if entered_pw != entered_pw2:  #validate passwords
                flash("Your passwords did not match")
                return redirect("/register")
            else:
            #update password into database
                new_user = User(password = entered_pw, email= entered_email, user_name = entered_username) 
                db.session.add(new_user)
                db.session.commit()
                print 'creating new user in Database.'
                print new_user, new_user.user_id
                session['email'] = entered_email
                flash("You are signed up %s!" % entered_email) 
                return redirect("/")
        else: 
            flash("You have already signed up with that email")
            return redirect('/login')




@app.route("/login")
def user_login():
    """Login page with form for users."""

    return render_template("login.html")




@app.route("/logout")
def process_logout():
    """Route to process logout for users."""

    return render_template("logout.html")




##################################
  		  #Info/ About
##################################


@app.route("/info")
def display_info():
    """General info and tips for users"""

    return render_template("info.html")



@app.route("/about")
def dispay_about():
    """General about page for users"""

    return render_template("about.html")



#######################################################

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()



