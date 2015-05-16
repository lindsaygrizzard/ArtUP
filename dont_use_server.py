









####
######
########

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Project, Wall, Wall_Art, Art, connect_to_db, db 

app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined




@app.route('/')
def index():
    """Homepage."""


    return render_template("homepage.html")


@app.route('/user-profile')
def list_projects():
    """Homepage."""

    # find current user id 
    cur_user_obj = User.query.filter(User.email == session['email']).first()
    cur_user_id = cur_user_obj.user_id
    projects = Project.query.filter(Project.user_id == cur_user_id).all()

    print "project: ", projects

    return render_template("user_profile.html", 
                        project_list=projects)







######################################
		   #PROJECT STUFF
######################################


# @app.route('/project')
# def project():
#     """Create new or select saved project"""

#     return render_template("project.html")


    
# @app.route('/project-process')
# def project_process():
#     """redirect based on choice"""

#     new_project = request.args.get("project_opt") 
#     print new_project
    
#     if new_project == "new":
#     	return redirect('/new-project')

#     else:
#     	return redirect('/user-profile')

 

# @app.route('/new-project')
# def project_name():
#     """List new project name"""
#     return render_template("new_project.html")


# @app.route('/new-project-process')
# def process_project_name():
#     """Store new project name"""

#     if 'email' in session:
#         print 'session: ', session
#         user_obj = User.query.filter(User.email == session['email']).first()
#         cur_user_id = user_obj.user_id
#         new_pro = request.args.get('new_project')

#         session['project_name'] = new_pro
#         print session

#         cur_pro_name = Project(
#             project_name = new_pro, 
#             user_id = cur_user_id)

#         db.session.add(cur_pro_name)
#         db.session.commit()

#         return redirect('/new-wall')

#     else:
#         return redirect('/login')
    

    
    ################################
             #WALL LIST STUFF
    ################################


# @app.route('/project/<int:project_id>')
# def show_project(project_id):

#     project_id = project_id

#     walls = Wall.query.filter(Wall.project_id == project_id).all()

#     print "walls: ", walls

#     return render_template("wall_list.html", 
#                         wall_list=walls,
#                         project_id= project_id)


# @app.route('/saved-project-new-wall/<project_id>')
# def get_saved_project_wall_info(project_id):
#     """Get wall information from saved project"""

#     project_obj = Project.query.filter_by(project_id = project_id).first()
#     cur_project_name = project_obj.project_name
#     print "CURRENT PROJECT NAME: ", cur_project_name

#     return render_template("saved_pro_new_wall.html", 
#                         project_name = cur_project_name)



# @app.route('/saved-project-new-wall-process')
# def process_saved_project_wall_info():
#     """Process wall information for saved project"""

#     project_obj = Project.query.filter(Project.project_name == session['project_name']).first()
#     cur_project_id = project_obj.project_id
#     print "PROJECT OBJECT ", project_name

#     if 'email' in session:

#         new_wall_name = request.args.get("new_wall")
#         wall_width = request.args.get("wall_width")
#         center_line = request.args.get("center_line")
#         #make unique names only be allowed
#         session['wall_name'] = new_wall_name
#         print "SESSION: ", session


#         cur_wall = Wall(
#                            wall_name = new_wall_name, 
#                            wall_width = int(wall_width), 
#                            center_line= int(center_line),
#                            project_id = int(cur_project_id))

#         db.session.add(cur_wall)
#         db.session.commit()
#         print "cur_wall", cur_wall


#         return redirect('/saved-wall-new-art')

#     else:
#         return redirect('/login')

    #ALSO ADD WALL_ID TO WALL_ART TABLE


            ############################
               # SAVED WALL ART STUFF
            ############################

# @app.route('/saved-wall-new-art')
# def get_saved_wall_art_info():
#     """Process art information for saved wall"""

#     return render_template("saved_wall_new_art.html")


# @app.route('/saved-wall-new-art-process')
# def process_saved_wall_art_info():
#     """Process art information for saved wall"""


#     wall_obj = Wall.query.filter(Wall.wall_name == session['wall_name']).first()
#     cur_wall_id = wall_obj.wall_id
#     print "wall_obj: ", wall_obj
#     print "cur_wall_id: ", cur_wall_id
#     print "session: ", session

#     if 'email' in session:
        
#         new_art_name = request.args.get("new_art")
#         print "new_art_name: ", new_art_name
#         art_height = request.args.get("art_height")
#         print "art_height: ", art_height
#         art_width = request.args.get("art_width")
#         print "art_width: ", art_width
#         # device = request.args.get("device_code")
#         # device_distance = request.args.get("device_distance")

#         session['art_name'] = new_art_name
#         print "New art name in session: ", session
#          #WHAT YOU KNOW WORK AND RETURN NONE?


#         cur_art = Art(
#             art_name = new_art_name,
#             height = int(art_height),
#             width = int(art_width)) 
#         db.session.add(cur_art)
#         db.session.commit()
#         print "Cur Art Obj: ", cur_art

#         art_obj = Art.query.filter(Art.art_name == cur_art.art_name).first()
#         print "ART OBJ: ", art_obj.art_id

#         art_id = art_obj.art_id
#         # cur_art_obj = art_obj.art_id


#         new_wall_art = Wall_Art(
#             art_id = art_id,
#             wall_id = cur_wall_id)

#         db.session.add(new_wall_art)
#         db.session.commit()
#         print "NEW WALL ART ID: ", new_wall_art

#         #ALSO ADD ART_ID TO WALL_ART TABLE
#         return redirect('/')


#     else:
#         return redirect("/login")




            ############################
             # END SAVED WALL ART STUFF
            ############################



    ################################
          # END WALL LIST STUFF
    ################################



######################################
		  # NEW WALL STUFF
######################################





@app.route('/new-wall')
def get_wall_info():
    """Get wall information"""
    return render_template("new_wall.html")


@app.route('/new-wall-process')
def process_wall_info():
    """Process wall information"""

    project_obj = Project.query.filter(Project.project_name == session['project_name']).first()
    cur_project_id = project_obj.project_id
    print "poject obj ", project_name

    if 'email' in session:
        if 'project_name' in session:
            new_wall_name = request.args.get("new_wall")
            wall_width = request.args.get("wall_width")
            center_line = request.args.get("center_line")
            #make unique names only be allowed
            session['wall_name'] = new_wall_name
            print "SESSION: ", session
            

            cur_wall = Wall(
                                wall_name = new_wall_name, 
                                wall_width = int(wall_width), 
                                center_line= int(center_line),
                                project_id = int(cur_project_id))

            db.session.add(cur_wall)
            db.session.commit()
            print "cur_wall", cur_wall

            
            return redirect('/artforms')

        else:
            return redirect('/login')



######################################
		   #ART STUFF
######################################


@app.route('/artforms')
def gather_art_info():
    """Gather art information"""

    return render_template("art_forms.html")


@app.route('/artforms-process')
def process_art_info():
    """Process art information"""

    wall_obj = Wall.query.filter(Wall.wall_name == session['wall_name']).first()
    cur_wall_id = wall_obj.wall_id
    print "wall_obj: ", wall_obj
    print "cur_wall_id: ", cur_wall_id
    print "session: ", session

    if 'email' in session:
        if 'project_name' in session:
            if 'wall_name' in session:
                new_art_name = request.args.get("new_art")
                print "new_art_name: ", new_art_name
                art_height = request.args.get("art_height")
                print "art_height: ", art_height
                art_width = request.args.get("art_width")
                print "art_width: ", art_width
                # device = request.args.get("device_code")
                # device_distance = request.args.get("device_distance")

                session['art_name'] = new_art_name
                print "New art name in session: ", session
                 #WHAT YOU KNOW WORK AND RETURN NONE?


                cur_art = Art(
                    art_name = new_art_name,
                    height = int(art_height),
                    width = int(art_width)) 
                db.session.add(cur_art)
                db.session.commit()
                print "Cur Art Obj: ", cur_art

                art_obj = Art.query.filter(Art.art_name == cur_art.art_name).first()
                print "ART OBJ: ", art_obj.art_id

                art_id = art_obj.art_id
                # cur_art_obj = art_obj.art_id


                new_wall_art = Wall_Art(
                    art_id = art_id,
                    wall_id = cur_wall_id)

                db.session.add(new_wall_art)
                db.session.commit()
                print "NEW WALL ART ID: ", new_wall_art

                return redirect('/')

            else:
                return redirect("/new-wall")
        else:
            return redirect("/project")

            return redirect('/')
    else:
        return redirect("/login")





# ##################################
#   #Calc_display/ Calculations
# ##################################


# @app.route('/calcdisplay/<int:wall_id>')
# def calcs(wall_id):
#     """Graphic Display of Calculations"""

#     return render_template("calc_display.html")




# @app.route('/calculations')
# def plain_calcs():
#     """Text only display of calculations"""

#     return render_template("calculations.html")





# ##################################
# 	#SIGN UP/ LOGIN/ SIGN OUT 
# ##################################


# @app.route("/register")
# def user_signup():
#     """Sign up a new user."""

#     return render_template("/register.html")

# #add jinja forms!
# @app.route("/register-process", methods=['POST'])
# def process_signup():
#     """Route to process login for users."""

#     entered_email = request.form['email']
#     entered_pw = request.form['password']
#     entered_pw2 = request.form['password2']
    
#     user = User.query.filter_by(email=entered_email).first()

#     if request.method == "POST":
#         if user == None: # is not in User Table?
#             if entered_pw != entered_pw2:  #validate passwords
#                 flash("Your passwords did not match")
#                 return redirect("/register")
#             else:
#             #update password into database
#                 new_user = User(password = entered_pw, email= entered_email) 
#                 db.session.add(new_user)
#                 db.session.commit()
#                 print 'creating new user in Database.'
#                 print new_user, new_user
#                 session['email'] = entered_email
#                 flash("You are signed up %s!" % entered_email) 
#                 return redirect("/")
#         else: 
#             flash("You have already signed up with that email")
#             return redirect('/login')




# @app.route("/login")
# def user_login():
#     """Login page with form for users."""

#     return render_template("login.html")


# @app.route("/login-process", methods=['POST'])
# def process_login():
#     """Route to process login for users."""

#     entered_email = request.form['email']
#     entered_pw = request.form['password']
    
#     user = User.query.filter_by(email= entered_email).first()

#     if user:
#         if entered_pw == user.password:
#             session['email'] = request.form['email']
#             print "session ", session
#             print "user ", user
#             flash('You successfully logged in %s!' % session['email'])
#             return redirect("/")
#         else:
#             flash("That is not the correct password!")
#             return redirect('/login')
#     else:
#         flash('That information was not found')
#         return redirect('login')



# @app.route("/logout")
# def process_logout():
#     """Route to process logout for users."""

    

#     session.pop('user_id', None)
#     session.pop('email', None)
#     flash('You successfully logged out!')
#     print "End Session: ", session
#     return redirect("/")






# ##################################
#   		  #Info/ About
# ##################################


# @app.route("/info")
# def display_info():
#     """General info and tips for users"""

#     return render_template("info.html")



# @app.route("/about")
# def dispay_about():
#     """General about page for users"""

#     return render_template("about.html")



# #######################################################

# if __name__ == "__main__":
#     # We have to set debug=True here, since it has to be True at the point
#     # that we invoke the DebugToolbarExtension
#     app.debug = True
#     app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

#     connect_to_db(app)

#     # Use the DebugToolbar
#     DebugToolbarExtension(app)

#     app.run()






