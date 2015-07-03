from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Project, Wall, Art, connect_to_db, db
import os


app = Flask(__name__)
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined

#########################################


@app.route('/')
def index():

    """Homepage."""

    if 'email' not in session:
        flash('You must Log In or Register before viewing projects')
    else:
        flash('Hello %s' % session['email'])
    return render_template('homepage.html')


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


@app.route('/project/<int:project_id>', methods=["GET", "POST"])
def show_project(project_id):

    """About project/ list of walls"""
    walls = Wall.query.filter(Wall.project_id == project_id).all()
    project_obj = Project.query.filter(project_id == Project.project_id).first()
    project_name = project_obj.project_name
    print "CURRENT PROJECT NAME: ", project_name

    return render_template("project.html",
                           wall_list=walls,
                           project_id=project_id,
                           project_name=project_name)


@app.route('/remove_project/<int:project_id>', methods=["GET", "POST"])
def delete_project(project_id):
    #query to delete row from db

    project_obj = Project.query.filter(Project.project_id == project_id).first()
    # db.session.delete(project_obj)
    # db.session.commit()
    print "AJAX project ID", project_id
    return jsonify({'project_id': project_id})


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
        project_disc = request.args.get('project_disc')

        session['project_name'] = new_pro

        cur_pro_name = Project(project_name=new_pro,
                               user_id=cur_user_id,
                               project_disc=project_disc)

        db.session.add(cur_pro_name)
        db.session.commit()

        print "CURRENT PROJECT NAME: ", cur_pro_name.project_name

        flash("You just created a NEW project named %s!" % cur_pro_name.project_name)
        return redirect('/user-profile')

    else:
        return redirect('/login')


@app.route('/remove_wall/<int:wall_id>', methods=["GET", "POST"])
def delete_wall(wall_id):

    """ Delete unwanted walls from db"""

    wall_obj = Wall.query.filter(Wall.wall_id == wall_id).first()
    print "WALL OBJ ", wall_obj
    art_objs = Art.query.filter(Art.wall_id == wall_id).all()
    print "ART OBJS THAT NEED TO BE DELECTED: ", art_objs

    # db.session.delete(wall_obj)
    # db.session.commit()
    print "AJAX WALL ID", wall_id

    return jsonify({'wall_id': wall_id})


@app.route('/project/<int:project_id>/new-wall')
def get_wall_info(project_id):

    """Get wall information from saved project"""

    if 'email' in session:
        project_obj = Project.query.filter(Project.project_id == project_id).first()
        cur_project_name = project_obj.project_name

        print "CURRENT PROJECT NAME FOR NEW WALL: ", cur_project_name

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
        wall_disc = request.args.get("wall_disc")
        wall_width = request.args.get("wall_width")
        width_fraction = request.args.get("wall_width_fraction")
        wall_height = request.args.get("wall_height")
        height_fraction = request.args.get("wall_height_fraction")
        center_line = request.args.get("center_line")
        center_fraction = request.args.get("center_line_fraction")
        offset_percent = request.args.get("offset_percent")
        wall_img = request.args.get("wall_img")
        session['wall_name'] = wall_name

        #format integers to pass to javascript
        adjusted_width = (int((int(wall_width) + float(width_fraction)) * 1000))
        adjusted_height = (int((int(wall_height) + float(height_fraction)) * 1000))
        adjusted_center = (int((int(center_line) + float(center_fraction)) * 1000))
        adjusted_offset = (int(float(offset_percent) * 1000))

        print "adjusted_width", adjusted_width
        print "adjusted_height", adjusted_height
        print "adjusted_center", adjusted_center
        print "offset_percent", offset_percent

        cur_wall = Wall(wall_name=wall_name,
                        wall_disc=wall_disc,
                        wall_width=adjusted_width,
                        wall_height=adjusted_height,
                        center_line=adjusted_center,
                        project_id=cur_project_id,
                        offset_percent=adjusted_offset,
                        wall_img=wall_img
                        )

        db.session.add(cur_wall)
        db.session.commit()

        wall_id = cur_wall.wall_id
        wall_name = cur_wall.wall_name

        print "CURRENT PROJECT NAME FOR  ART FORM: ", project_obj.project_name
        print "CURRENT WALL NAME FOR  ART FORM: ", wall_name

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
        cur_wall_name = cur_wall_obj.wall_name
        print "CURRENT WALL NAME: ", cur_wall_name

        new_art_name = request.args.get("new_art")
        art_height = request.args.get("art_height")
        height_fraction = request.args.get("art_height_fraction")
        art_width = request.args.get("art_width")
        width_fraction = request.args.get("art_width_fraction")
        device_code = request.args.get("device_code")
        device_distance = request.args.get("device_distance")
        device_fraction = request.args.get("art_device_fraction")
        art_img = request.args.get("img")

        print "NEW ART NAME: ", new_art_name
        session['art_name'] = new_art_name

        adjusted_width = (int((int(art_width) + float(width_fraction)) * 1000))
        adjusted_height = (int((int(art_height) + float(height_fraction)) * 1000))
        adjusted_device = (int((int(device_distance) + float(device_fraction)) * 1000))
        print "ART adjusted_width: ", adjusted_width
        print "ART adjusted_height: ", adjusted_height
        print "ART adjusted_device: ", adjusted_device

        #save info to Art table
        cur_art = Art(wall_id=wall_id,
                      art_name=new_art_name,
                      art_height=adjusted_height,
                      art_width=adjusted_width,
                      device_code=device_code,
                      device_distance=adjusted_device,
                      art_img=art_img)

        db.session.add(cur_art)
        db.session.commit()

        #get art object info just committed
        art_obj = Art.query.filter(Art.art_name == cur_art.art_name).first()
        art_id = art_obj.art_id

        submit_option = request.args.get("submit")
        if submit_option == "submit and display":
            return render_template('generate.html',
                                   wall_id=wall_id)

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

    cur_wall_obj = Art.query.filter(Art.wall_id == wall_id).first()
    cur_wall_id = cur_wall_obj.wall_id

    if cur_wall_obj is None:
        flash("No art found, make new wall")
        return redirect('/')
    else:
        return render_template('generate.html',
                               wall_id=cur_wall_id)


@app.route('/calcdisplay/<int:wall_id>')
def calcs(wall_id):

    """Query and pass all calculating information """

    cur_wall_id = wall_id
    cur_wall_obj = Wall.query.filter(Wall.wall_id == cur_wall_id).first()
    print "cur_wall_obj: ", cur_wall_obj
    art_objs = Art.query.filter(Art.wall_id == cur_wall_id).all()
    print "art Objs: ", art_objs

    #prep for javascript
    wall = cur_wall_obj.__dict__
    #pop off unwanted object
    wall.pop('_sa_instance_state')

    art = []
    for i in art_objs:
        a = i.__dict__
        if '_sa_instance_state' in a:
            a.pop('_sa_instance_state')
        art.append(a)
        print "Art LIST: ", art
    return render_template("calc_display.html", wall=wall, art=art)




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

    print "entered_email", entered_email
    print "entered_pw", entered_pw
    print "entered_pw2", entered_pw2

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
            return redirect("/user-profile")
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
    PORT = int(os.environ.get("PORT", 5432))

    app.debug = True
    connect_to_db(app)
    app.run()
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
