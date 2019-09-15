from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_jsglue import JSGlue
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp


from helpers import *

# configure application
app = Flask(__name__)
JSGlue(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response



# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///cooking.db")

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/about_us")
def about_us():
    return apology("website built by cats")

@app.route("/best")
def best():

    if request.args.get('category') != None:
        category=request.args.get('category')
        rows= db.execute("SELECT * FROM recipes JOIN users ON recipes.user=users.id WHERE category = :category ORDER BY rating_average DESC",category=category)
        return render_template("best.html", recipes = rows)


    rows= db.execute("SELECT * FROM recipes JOIN users ON recipes.user=users.id ORDER BY rating_average DESC")
    return render_template("best.html", recipes = rows)



@app.route("/changepass", methods=["POST"])
def changepass():
    oldhash = db.execute("SELECT hash FROM users WHERE id=:id", id=session["user_id"])

    if len(request.form["newpassword"]) < 5:
        return apology("New password must be at least 5 characters long")

    if request.form["newpassword"].isalnum() == False:
        return apology("New password must be alphanumeric")

    if pwd_context.verify(request.form.get("oldpassword"), oldhash[0]["hash"]):
        newhash= pwd_context.hash(request.form["newpassword"])
        db.execute("UPDATE users SET hash=:hash WHERE id=:id", id=session["user_id"],hash=newhash)
        return apology("password changed")
    else:
        return apology("oldpassword is incorrect")


@app.route("/comment", methods=["POST"])
@login_required
def comment():
    db.execute("INSERT INTO comments (content, recipe_id, user_id, date) VALUES (:content, :recipe_id, :user_id, CURRENT_TIMESTAMP)", content = request.form["comment"], recipe_id= request.form["recipe_id"], user_id= session["user_id"])
    db.execute("UPDATE recipes SET comment_number = comment_number + 1 WHERE id_r=:id_r",id_r = request.form["recipe_id"])
    return apology("commented")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/makerecipe")
@login_required
def makerecipe():
    return render_template("makerecipe.html")

@app.route("/myaccount")
@login_required
def myaccount():
    rows = db.execute("SELECT * FROM users WHERE id=:id", id= session["user_id"])
    return render_template("myaccount.html", users = rows)

@app.route("/myrecipes")
@login_required
def myrecipes():
    rows = db.execute("SELECT * FROM recipes WHERE user=:user", user=session["user_id"])
    return render_template("myrecipes.html", recipes = rows)

@app.route("/rate", methods=["POST"])
@login_required
def rate():
    db.execute("INSERT INTO ratings (rating, recipe_id) VALUES (:rating, :recipe_id)", rating=request.form["star"] , recipe_id=request.form["recipe_id"])
    rows = db.execute("SELECT rating FROM ratings WHERE recipe_id = :recipe_id", recipe_id = request.form["recipe_id"])

    ratings_number = len(rows)

    ratings_sum = db.execute("SELECT SUM(rating) AS sum FROM ratings WHERE recipe_id = :recipe_id", recipe_id = request.form["recipe_id"])


    rating_average = ratings_sum[0]["sum"]/ratings_number



    db.execute("UPDATE recipes SET rating_number=:rating_number, rating_average=:rating_average WHERE id_r= :id_r", rating_number= ratings_number, rating_average= rating_average, id_r=request.form["recipe_id"])

    return apology("Your rating has been registered")


@app.route("/recipe")
def recipe():
    recipe_id = request.args.get('id')
    rows = db.execute("SELECT * FROM recipes JOIN users ON recipes.user=users.id WHERE id_r= :id_r", id_r=recipe_id)
    rows2 = db.execute("SELECT * FROM comments JOIN users ON comments.user_id=users.id WHERE recipe_id=:recipe_id", recipe_id=recipe_id)
    if len(rows)==0:
        return apology("Recipe not found")


    ratingpercent= (rows[0]["rating_average"]/5)*100
    db.execute("UPDATE recipes SET views=views + 1 WHERE id_r = :id_r", id_r=recipe_id)
    return render_template("recipe.html", recipes = rows, comments=rows2, rating=ratingpercent)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register_recipe", methods= ["POST"])
def register_recipe():
    if request.form["title"]=="" or request.form["time"]=="" or request.form["difficulty"]== "" or request.form["recipe"]== "" :
        return apology("Must fill out all fields")

    db.execute("INSERT INTO recipes (title, content, picture, time, difficulty, date, user, category) VALUES (:title, :content, :picture, :time, :difficulty, CURRENT_TIMESTAMP, :user, :category)", title = request.form["title"], content = request.form["recipe"], picture=request.form["picture"], time = request.form["time"], difficulty= request.form["difficulty"], user = session["user_id"], category= request.form["category"])
    return apology("recipe registered")
@app.route("/registering", methods= ["POST"])
def registering():
   #encrypts inputted password
    hashpass = pwd_context.hash(request.form["hash"])
    #checks if password or username are blank
    if request.form["username"]=="" or request.form["hash"]=="" :
        return apology("Must provide username and password")

    #checks if password and password confirmation fields match
    if request.form["hash"] != request.form["hashconfirm"]:
        return apology("Passwords do not match")

   #checks password length
    if len(request.form["hash"]) < 5:
        return apology("Password must be at least 5 characters long")

    if request.form["hash"].isalnum() == False:
        return apology("Password must be alphanumeric")
    #if all good, registers user
    else:
        x = db.execute("SELECT * FROM users WHERE username = :username", username=request.form["username"])
        if len(x) == 0:
            y = db.execute("SELECT * FROM users WHERE email = :email", email=request.form["email"])
            if len(y) == 0:
                db.execute("INSERT INTO users (username, hash, email) VALUES (:username, :hash, :email)", username=request.form["username"], hash=hashpass, email=request.form["email"])
                return apology("Good")
            else:
                return apology("E-mail already in use")
        else:
            return apology("Username already exists")

@app.route("/search")
def search():
    """Search for recipes that match query."""
    q = request.args.get("q") + "%"
    something = db.execute("""SELECT title, id_r FROM recipes
            WHERE title LIKE :q
            GROUP BY title
            ORDER BY RANDOM()
            LIMIT 10""", q = q)

    if not request.args.get("q"):
        raise RuntimeError;

    return jsonify(something)