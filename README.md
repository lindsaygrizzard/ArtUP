# ArtUP
ArtUP is a art hanging application and repository that allows professional galleries 
and the DIY weekend warrior alike to mathematically generate virtual art installations. 
Users have the freedom to alter the standard generated output and track their changes. 
Hanging art work properly can be time consuming and lead to damaged walls if not done 
meticulously. ArtUP allows the user to curate an entire show or decorate their house 
before ever drilling into the wall. 

<h4> Technology Stack </h4>

JavaScript, jQuery, D3, AJAX, Python, Flask, Jinja, SQLAlchemy, SQLite, HTML, CSS

![artup_app_demo](https://cloud.githubusercontent.com/assets/10122766/8068509/1b84ef9a-0ea9-11e5-887e-d05e1d206b28.gif)


<h4> Creating a Project/ Viewing a saved project folder </h4>
Each User can create multiple project repositories. These 'folders' can be used by galleries for an exhibition or the
home user for a living room or kitchen project. 
![screen shot 2015-06-09 at 1 14 47 pm](https://cloud.githubusercontent.com/assets/10122766/8068603/c4d26de8-0ea9-11e5-960f-2df540395561.png)

<h4> Creating a Wall/ Viewing a saved Wall </h4>

Each Project contains user created and customized walls. For example the "South Wall" of a room or gallery space. 
The user can customize their walls with an image of their choice, the invisible 'center line' running through all
pieces of art, and the wall dimensions. 

![screen shot 2015-06-09 at 12 29 14 am](https://cloud.githubusercontent.com/assets/10122766/8068605/c7927f5a-0ea9-11e5-8ff8-df01d75b4186.png)
![screen shot 2015-06-09 at 12 37 26 am](https://cloud.githubusercontent.com/assets/10122766/8068615/d1544776-0ea9-11e5-9187-871bf90681a5.png)

<h4> Viewing your Art Hangings </h4>

When the user creates a new wall they will be directed to an art forms page. Here they can specify each piece of art they would like included on their wall. 
After hitting submit, the app will run a series of calculations to determine the balanced hanging composition and return
the x and y coordinates (in fractions specific to a measuring tape) of each "screw point" of each artwork or the corner point if no screw point exists. 

It will also render a visual representation of the specific dimensions of wall and artworks using D3 and 
multiple calculations in js to render a user friendly and representative interaction

![screen shot 2015-06-09 at 1 17 16 pm](https://cloud.githubusercontent.com/assets/10122766/8068631/f9765d20-0ea9-11e5-8075-46741556d4b5.png)

<h4> But what if I want to be more creative with my art hanging design?! </h4>

Using the D3 drag feature and in depth DOM manipulation, the user can drag each art piece to their desired location.
This process keeps track of the left and right margins regardless of which piece is moved for easy design balance. 

![screen shot 2015-06-09 at 1 17 24 pm](https://cloud.githubusercontent.com/assets/10122766/8068633/fcec57f2-0ea9-11e5-9f2b-af276aeb843d.png)
