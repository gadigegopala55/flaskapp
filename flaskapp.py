import sqlite3
from flask import *
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app) # instantiate the mail class
   
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "demomail224@gmail.com"
app.config['MAIL_PASSWORD'] = "oxuitzgzzerxsgam"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#creating a admin database
@app.route("/create")
def create():
    try:
        connection = sqlite3.connect("admin.db")
        conn = connection.cursor()
        conn.execute("CREATE TABLE IF NOT EXISTS admin(id INTEGER PRIMARY KEY,userid VARCHAR(40),password VARCHAR(40),userlogin VARCHAR(40))")
        return "<h1>Successfull<h1>"
    except:
        return "Something Went Wrong"

#inserting a admin data(userid,password)
@app.route("/insert")
def insert():
    try:
        connection = sqlite3.connect("admin.db")
        conn = connection.cursor()
        conn.execute('INSERT INTO admin VALUES(1,"gopal","krishna","failure")')
        connection.commit()
        return "<h1>Data Entered successfully<h1>"
    except:
        return "Something Went Wrong"

#creating a post database
@app.route("/createpost")
def createpost():
    try:
        connection = sqlite3.connect("post.db")
        conn = connection.cursor()
        conn.execute("CREATE TABLE IF NOT EXISTS post(title VARCHAR(400),description VARCHAR(400))")
        return "<h1>Successfull<h1>"
    except:
        return "Something Went Wrong"

#Home Page
@app.route("/")
def home():
    try:
        connection = sqlite3.connect("post.db")
        conn = connection.cursor()
        conn.execute("SELECT * FROM post")
        mydata = conn.fetchall()
        return render_template("home.html",mydata = mydata)
    except:
        return "Something Went Wrong"

#Login Page
@app.route("/login",methods=["GET","POST"])
def login():
    connection = sqlite3.connect("admin.db")
    conn = connection.cursor()
    conn.execute("SELECT * FROM admin")
    mydata = conn.fetchone()
    data = mydata[3]
    if data == "failure":
        if request.method == "POST":
            userid = request.form['userid']
            password = request.form['password']
            if userid == "gopal" and password == "krishna":
                conn.execute("UPDATE admin SET userlogin='success'")
                connection.commit()
                return redirect("/post")
            else:
                return render_template("login.html",message="* Enter valid Details")
    else:
        return redirect("/post")
    return render_template("login.html",message="")

# Posting a blog
@app.route("/post",methods=["GET","POST"])
def post():
    try:
        connection = sqlite3.connect("admin.db")
        conn = connection.cursor()
        conn.execute("SELECT * FROM admin")
        mydata = conn.fetchone()
        data = mydata[3]
        if data == "failure":
            return redirect("/login")
        else:
            if request.method == "POST":
                title = request.form["title"]
                description = request.form["description"]
                if not title or not description:
                    return render_template("post.html",message="* Enter all fields")
                connection = sqlite3.connect("post.db")
                conn = connection.cursor()
                conn.execute(f'INSERT INTO post VALUES("{title}","{description}")')
                connection.commit()
                connection = sqlite3.connect("admin.db")
                conn = connection.cursor()
                conn.execute("SELECT * FROM subscribers")
                mydata = conn.fetchall()
                for char in mydata:
                    mailid = char[1]
                    msg = Message(
                        'Traveling Blog',
                        sender ='demomail224@gmail.com',
                        recipients = [f'{mailid}']
                    )
                    msg.body = f'Gopala Krishna posted new post on "{title}"'
                    mail.send(msg)
                return render_template("post.html",message="Successfully Posted the data")
            return render_template("post.html",message="")
        return redirect("/login")
    except:
        return render_template("post.html",message="Something Went Wrong")

#Deleting a post
@app.route("/delete",methods=["GET","DELETE"])
def delete():
    try:
        connection = sqlite3.connect("admin.db")
        conn = connection.cursor()
        conn.execute("SELECT * FROM admin")
        mydata = conn.fetchone()
        data = mydata[3]
        if data == "failure":
            return redirect("/login")
        else:
            name = request.args.get("title")
            if not name:
                return render_template("delete.html",message="* Enter Title")
            connection = sqlite3.connect("post.db")
            conn = connection.cursor()
            conn.execute(f'SELECT * FROM post WHERE title="{name}"')
            mydata = conn.fetchall()
            length = len(mydata)
            if length == 0:
                return render_template("delete.html",message="* Enter valid title")
            else:
                conn.execute(f'DELETE FROM post WHERE title="{name}"')
                connection.commit()
                return render_template("delete.html",message="Deleted data successfully")
        return render_template("delete.html",message="")
    except:
        return render_template("delete.html",message = "Something Went Wrong")

#Updating a post
@app.route("/put",methods=["GET","PUT"])
def put():
    try:
        connection = sqlite3.connect("admin.db")
        conn = connection.cursor()
        conn.execute("SELECT * FROM admin")
        mydata = conn.fetchone()
        data = mydata[3]
        if data == "failure":
            return redirect("/login")
        else:
            name = request.args.get("title")
            description = request.args.get("description")
            if not name or not description:
                return render_template("put.html",message="* Enter all fields")
            connection = sqlite3.connect("post.db")
            conn = connection.cursor()
            conn.execute(f'SELECT * FROM post WHERE title="{name}"')
            mydata = conn.fetchall()
            length = len(mydata)
            if length == 0:
                return render_template("put.html",message = "* Enter valid title")
            else:
                conn.execute(f'UPDATE post SET description="{description}" WHERE title="{name}"')
                connection.commit()
                return render_template("put.html",message = "Successfully updated the Post")
        return render_template("put.html",message="")
    except:
        return render_template("put.html",message = "Something Went Wrong")

#Logout API
@app.route("/logout")
def logout():
    try:
        connection = sqlite3.connect("admin.db")
        conn = connection.cursor()
        conn.execute("UPDATE admin SET userlogin='failure'")
        connection.commit()
        return redirect("/login")
    except:
        return "Something Went Wrong"

# creating the subscription table
@app.route("/createsubscriber")
def createsubscriber():
    try:
        connection = sqlite3.connect("admin.db")
        conn = connection.cursor()
        conn.execute("CREATE TABLE IF NOT EXISTS subscribers(name VARCHAR(40),email VARCHAR(40),phonenumber INTEGER)")
        return "<h1>Successfull<h1>"
    except:
        return "Something Went Wrong"

#Adding subcribers data
@app.route("/subscribe",methods = ["GET","POST"])
def subscribe():
    try:
        if request.method == "POST":
            name = request.form['name']
            email = request.form['email']
            phonenumber = request.form['phonenumber']

            if not name or not email or not phonenumber:
                return render_template("subscribe.html",message="* Enter all fields")
        
            connection = sqlite3.connect("admin.db")
            conn = connection.cursor()
    
            msg = Message(
                'Traveling Blog Notification',
                sender ='demomail224@gmail.com',
                recipients = [f'{email}']
            )
            msg.body = f'Thank you {name} , You will receive the Notification whenever new Post is Posted in Blog'
            mail.send(msg)
            conn.execute(f'INSERT INTO subscribers VALUES("{name}","{email}",{phonenumber})')
            connection.commit()
            return render_template("subscribe.html",message = "You are subscribed")
        return render_template("subscribe.html",message="")
    except:
        return render_template("subscribe.html",message=" * Enter valid Email")

# creating the comment table
@app.route("/createcomment")
def createcomment():
    try:
        connection = sqlite3.connect("admin.db")
        conn = connection.cursor()
        conn.execute("CREATE TABLE IF NOT EXISTS comment(name VARCHAR(40),comment VARCHAR(400))")
        return "<h1>Successfull<h1>"
    except:
        return "Something Went Wrong"

#Adding a Comment
@app.route("/comment",methods = ["GET","POST"])
def comment():
    try:
        if request.method == "POST":
            name = request.form['name']
            comment = request.form['comment']

            if not name or not comment:
                return render_template("comment.html",message="*Enter all fields")
        
            connection = sqlite3.connect("admin.db")
            conn = connection.cursor()
            conn.execute(f'INSERT INTO comment VALUES("{name}","{comment}")')
            connection.commit()
            return render_template("comment.html",message="Commented Successfully")
        return render_template("comment.html",message="")
    except:
        return render_template("comment.html",message = "Somethoing Went Wrong")

#Read Comment
@app.route("/readcomment")
def readcomment():
    try:
        connection = sqlite3.connect("admin.db")
        conn = connection.cursor()
        conn.execute("SELECT * FROM comment")
        mydata = conn.fetchall()
        return render_template("readcomment.html",mydata = mydata)
    except:
        return "Something Went Wrong"

# getting the subscription data
@app.route("/subscriberslist")
def subscriberslist():
    try:
        connection = sqlite3.connect("admin.db")
        conn = connection.cursor()
        conn.execute("SELECT * FROM admin")
        mydata = conn.fetchone()
        data = mydata[3]
        if data == "failure":
            return redirect("/login")
        else:
            connection = sqlite3.connect("admin.db")
            conn = connection.cursor()
            conn.execute("SELECT * FROM subscribers")
            mydata = conn.fetchall()
            return render_template("subscriberslist.html",mydata = mydata)
        return render_template("subscriberslist.html",mydata = mydata)
    except:
        return "Something Went Wrong"

#subscribers data delete
@app.route("/subscriberdelete")
def subscribersdelete():
    try:
        connection = sqlite3.connect("admin.db")
        conn = connection.cursor()
        conn.execute("SELECT * FROM admin")
        mydata = conn.fetchone()
        data = mydata[3]
        if data == "failure":
            return redirect("/login")
        else:
            name = request.args.get("name")
            if not name:
                return render_template("subscriberdelete.html",message="* Enter Name")
            connection = sqlite3.connect("admin.db")
            conn = connection.cursor()
            conn.execute(f'SELECT * FROM subscribers WHERE name="{name}"')
            mydata = conn.fetchall()
            length = len(mydata)
            if length == 0:
                return render_template("delete.html",message = "* Enter valid name")
            else:
                conn.execute(f'DELETE FROM subscribers WHERE name="{name}"')
                connection.commit()
                return render_template("delete.html",message = "Deleted data successfully")
        return render_template("delete.html",message = "")
    except:
        return "Something Went Wrong"


if __name__=="__main__":
    app.run(debug=True)