from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Project, Wall, Wall_Art, Art, connect_to_db, db


app = Flask(__name__)
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined

#########################################


@app.route('/')
def index():

    """Homepage."""

    # print "SESSION", session
    return render_template("homepage.html")


@app.route('/user-profile')
def list_projects():

    """User Profile and list of projects"""

    if 'email' in session:
        cur_user_obj = User.query.filter(User.email == session['email']).first()
        cur_user_id = cur_user_obj.user_id
        cur_user_email = cur_user_obj.email
        projects = Project.query.filter(Project.user_id == cur_user_id).all()
        return render_template("user_profile.html",
                               project_list=projects,
                               email=cur_user_email)
    else:
        flash('You must Log In or Register before viewing projects')
        return render_template('homepage.html')


@app.route('/project/<int:project_id>')
def show_project(project_id):

    """About project/ list of walls"""

    walls = Wall.query.filter(Wall.project_id == project_id).all()
    project_obj = Project.query.filter(project_id == Project.project_id).first()
    project_name = project_obj.project_name
    # print "PROJECT ID: ", project_id
     # print "PROJECT OBJ: ", project_obj
    # print "PROJECT NAME: ", project_name
    return render_template("project.html",
                           wall_list=walls,
                           project_id=project_id,
                           project_name=project_name)


@app.route('/project/<int:project_id>/new-wall')
def get_wall_info(project_id):

    """Get wall information from saved project"""

    if 'email' in session:
        project_obj = Project.query.filter(Project.project_id == project_id).first()
        cur_project_name = project_obj.project_name
        # print "CURRENT PROJECT NAME: ", cur_project_name
        return render_template("new_wall.html",
                               project_id=project_id,
                               project_name=cur_project_name)
    else:
        flash("You must log in or register to create projects")
        redirect('/')


@app.route('/project/<int:project_id>/wall_process/artform')
def process_wall_info(project_id):

    """Process wall information and show artform page"""

    if 'email' in session:
        project_obj = Project.query.filter(Project.project_id == project_id).first()
        cur_project_id = project_obj.project_id
        wall_name = request.args.get("new_wall")
        wall_width = request.args.get("wall_width")
        wall_height = request.args.get("wall_height")
        center_line = request.args.get("center_line")
        session['wall_name'] = wall_name
        # print "PROJECT OBJECT:   ", project_obj
        # print "PROJECT ID ", cur_project_id
        # print "SESSION: ", session

        cur_wall = Wall(wall_name=wall_name,
                        wall_width=wall_width,
                        wall_height=wall_height,
                        center_line=center_line,
                        project_id=cur_project_id
                        )

        db.session.add(cur_wall)
        db.session.commit()

        wall_id = cur_wall.wall_id
        wall_name = cur_wall.wall_name

        return render_template("new_art.html",
                               project_id=project_id,
                               wall_id=wall_id,
                               wall_name=wall_name)
    else:
        flash("You must log in or register to create projects")
        redirect('/')


@app.route('/project/<int:project_id>/wall/<int:wall_id>/process_art_form')
def process_art_info(project_id, wall_id):

    """Process wall information for saved project and show calc_display/ more artforms"""

    if 'email' in session:
        cur_wall_obj = Wall.query.filter(wall_id == Wall.wall_id).first()
        cur_wall_id = cur_wall_obj.wall_id
        cur_wall_name = cur_wall_obj.wall_name
        print "WALL ID: ", wall_id

        new_art_name = request.args.get("new_art")
        art_height = request.args.get("art_height")
        art_width = request.args.get("art_width")
        device_code = request.args.get("device_code")
        device_distance = request.args.get("device_distance")

        session['art_name'] = new_art_name

        #save info to Art table
        cur_art = Art(art_name=new_art_name,
                      art_height=art_height,
                      art_width=art_width,
                      device_code=device_code,
                      device_distance=device_distance)

        db.session.add(cur_art)
        db.session.commit()

        #get art object info just committed
        art_obj = Art.query.filter(Art.art_name == cur_art.art_name).first()
        art_id = art_obj.art_id

        new_wall_art = Wall_Art(art_id=art_id,
                                wall_id=cur_wall_id)

        db.session.add(new_wall_art)
        db.session.commit()

        wall_art_obj = Wall_Art.query.filter(Wall_Art.art_id == art_id).first()
        wall_art_id = wall_art_obj.art_id

        submit_option = request.args.get("submit")
        if submit_option == "submit and display":
            return render_template('generate.html',
                                   wall_art_id=wall_art_id)

        else:
            return render_template('new_art.html',
                                   wall_name=cur_wall_name,
                                   project_id=project_id,
                                   wall_id=wall_id)
    else:
        flash("You must log in or register to create projects")
        redirect('/')


@app.route('/saved_wall_process/<int:wall_id>')
def saved_wall_process(wall_id):

    """processes and formats saved wall data"""

    cur_wall_art_obj = Wall_Art.query.filter(Wall_Art.wall_id == wall_id).first()
    cur_wall_art_id = cur_wall_art_obj.wall_art_id

    if cur_wall_art_obj is None:
        flash("No art found, make new wall")
        return redirect('/')
    else:
        return render_template('generate.html',
                               wall_art_id=cur_wall_art_id)


@app.route('/calcdisplay/<int:wall_art_id>')
def calcs(wall_art_id):

    """Graphic Display of Calculations"""

    #current ref obj
    cur_ref_obj = Wall_Art.query.filter(Wall_Art.wall_art_id == wall_art_id).first()
    cur_wall_id = cur_ref_obj.wall_id
    cur_wall_obj = Wall.query.filter(Wall.wall_id == cur_wall_id).first()
    ref_by_wall_obj = Wall_Art.query.filter(Wall_Art.wall_id == cur_wall_id).all()
    wall_width = cur_wall_obj.wall_width
    art_objs = Art.query.filter(Art.art_id == Wall_Art.art_id).all()

    #prep for javascript
    wall = cur_wall_obj.__dict__
    #pop off unwanted object
    wall.pop('_sa_instance_state')

    #FOR MVP (REMOVE ON NEXT ITERATION TO ALOW MORE ART THAN WALL)
    art_ids = []
    for obj in ref_by_wall_obj:
        art_id = obj.art_id
        art_ids.append(art_id)
    art_objs = []
    for num in art_ids:
        art_obj = Art.query.filter(Art.art_id == num).first()
        art_objs.append(art_obj)
    art_widths = []
    for i in art_objs:
        art_widths.append(art_obj.art_width)
        if sum(art_widths) >= wall_width:
            db.session.delete(cur_ref_obj)
            flash("Art width exceeds wall space")
            return render_template("homepage.html")

        else:
            art = []
            for i in art_objs:
                a = i.__dict__
                a.pop('_sa_instance_state')
                art.append(a)
            return render_template("calc_display.html", wall=wall, art=art)


@app.route('/new-project')
def project_name():

    """List new project name"""

    return render_template("new_project.html")


@app.route('/new-project-process')
def process_project_name():

    """Store new project name"""

    if 'email' in session:
        user_obj = User.query.filter(User.email == session['email']).first()
        cur_user_id = user_obj.user_id
        new_pro = request.args.get('new_project')

        session['project_name'] = new_pro

        cur_pro_name = Project(project_name=new_pro,
                               user_id=cur_user_id)

        db.session.add(cur_pro_name)
        db.session.commit()

        project_obj = Project.query.filter(Project.project_name == session['project_name']).first()
        cur_project_name = project_obj.project_name
        # print "PROJECT OBJECT: ", project_obj
        # print "PROJECT ID: ", cur_project_name

        flash("You just created a NEW project named %s!" % cur_project_name)
        return redirect('/user-profile')

    else:
        return redirect('/login')


##################################
    #SIGN UP/ LOGIN/ SIGN OUT
##################################


@app.route("/register")
def user_signup():

    """Sign up a new user."""

    return render_template("/register.html")


@app.route("/register-process", methods=['POST'])
def process_signup():

    """Route to process login for users."""

    entered_email = request.form['email']
    entered_pw = request.form['password']
    entered_pw2 = request.form['password2']

    user = User.query.filter_by(email=entered_email).first()

    if request.method == "POST":
        if user is None:
            #validate pw better later
            if entered_pw != entered_pw2:
                flash("Your passwords did not match")
                return redirect("/register")
            else:
                new_user = User(password=entered_pw, email=entered_email)
                db.session.add(new_user)
                db.session.commit()
                print 'creating new user in Database.'
                print new_user, new_user
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


@app.route("/login-process", methods=['POST'])
def process_login():

    """Route to process login for users."""

    entered_email = request.form['email']
    entered_pw = request.form['password']

    user = User.query.filter_by(email=entered_email).first()

    if user:
        if entered_pw == user.password:
            session['email'] = request.form['email']
            flash('You successfully logged in %s!' % session['email'])
            return redirect("/")
        else:
            flash("That is not the correct password!")
            return redirect('/login')
    else:
        flash('That information was not found')
        return redirect('login')


@app.route("/logout")
def process_logout():

    """Route to process logout for users."""

    session.pop('user_id', None)
    session.pop('email', None)
    flash('You successfully logged out!')
    return redirect("/")


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
