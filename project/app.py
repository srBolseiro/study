import os
import sqlite3
import re

from cs50 import SQL
from flask import Flask, flash, redirect, url_for, render_template, request, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config.from_object(__name__)
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

# Configure email validation
EMAIL_PATTERN = r"^[\w\.-]+@[\w\.-]+\.\w+$"
SUPPORTED_GAMES = ["vampire_v5",]

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    if session.get("user_id") is None:
        return render_template("home.html", sheets="", supported=SUPPORTED_GAMES)
    else:
        sheets = db.execute("SELECT * FROM player_sheets WHERE user_id = ?", session["user_id"])
        return render_template("home.html", sheets=sheets, supported=SUPPORTED_GAMES)


#  Register
@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if session.get("user_id") is None:
            return render_template("register.html")
        else:
            return redirect(url_for("index"))
    else:
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        c_password = request.form.get("c_password")

        # Input validation
        # Check for null
        if not username or not email or not password or not c_password:
            flash("Must fill all fields!", "danger")
            return redirect(url_for("register"))
        # Check for length
        if len(username) < 4 or len(username) > 20 or len(password) < 8 or len(password) > 16 or len(c_password) < 8 or len(c_password) > 16:
            flash("Username size must be between 4 and 20. Password size must be between 8 and 16", "danger")
            return redirect(url_for("register"))
        # Check password match
        if password != c_password:
            flash("Passwords didn't match!", "danger")
            return redirect(url_for("register"))
        # Check for valid email
        if not re.match(EMAIL_PATTERN, email):
            flash("Invalid email!", "danger")
            return redirect(url_for("register"))
        else:
            query = db.execute("SELECT username FROM users WHERE username = ?", username)
            if query:
                flash("Username already registered!", "danger")
                return redirect(url_for("register"))
            else:
                hashed = generate_password_hash(password)
                db.execute("INSERT INTO users (username, email, hash) VALUES (?, ?, ?)", username, email, hashed)
                flash("Success", "success")
                return redirect(url_for("login"))


# Login
@app.route("/login/", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        if session.get("user_id") is None:
            return render_template("login.html")
        else:
            return redirect(url_for("index"))
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        # Input validation
        if not username or not password:
            flash("Must fill all fields!", "error")
            return redirect(url_for("login"))
        if len(username) < 4 or len(username) > 20 or len(password) < 8 or len(password) > 16:
            flash("Username size must be between 4 and 20. Password size must be between 8 and 16", "error")
            return redirect(url_for("login"))

        # Query DB for data
        db_user = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Check if match
        if not db_user:
            flash("User not found!", "error")
            return redirect(url_for("login"))

        if username == db_user[0]["username"]:
            if check_password_hash(db_user[0]["hash"], password):
                session["user_id"] = db_user[0]["id"]
                return redirect(url_for("index"))
            else:
                flash("Incorrect password", "error")
                return redirect(url_for("login"))
        else:
            flash("User not found", "error")
            return redirect(url_for("login"))


@app.route("/logout/")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# Player sheets
@app.route("/player/", methods=["GET", "POST"])
@login_required
def player():
    if request.method == "GET":
        query = db.execute("SELECT * FROM player_sheets WHERE user_id = ?", session["user_id"])
        return render_template("player.html", games=query)
    else:
        pick = request.form.get("sheet_id")
        game = db.execute("SELECT * FROM player_sheets WHERE sheet_id = ?", pick)
        if game[0]["game"] == "vampire_v5":
            return redirect(url_for("vampire_v5", sheet_id=pick))
        else:
            return "game not supported :/"


@app.route("/create/", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "GET":
        return render_template("create.html", games=SUPPORTED_GAMES)
    else:
        game_name = request.form.get("game")
        if game_name == SUPPORTED_GAMES[0]:
            return redirect(url_for("create_sheet", game=game_name))
        else:
            return "game not supported"


@app.route("/create/<game>/", methods=["GET", "POST"])
@login_required
def create_sheet(game):
    if request.method == "GET":
        if game == SUPPORTED_GAMES[0]:
            return render_template("/sheets/vamp_v5/vampire_v5_creator.html")
        else:
            return "game not supported"
    else:
        request.form
        # insert into vampire_v5
        db.execute("""INSERT INTO vampire_v5 (characterName, user_id, concept, chronicle, playerName, clan,generation,strength,
                   dexterity,stamina,charisma,manipulation,composure,intelligence,wits,resolve,athletics,brawl,craft,drive,
                   firearms,larceny,melee,stealth,survival,animalKen,etiquette,insight,intimidation,leadership,performance,
                   persuasion,streetwise,subterfuge,academics,awareness,finance,investigation,medicine,occult,politics,
                   science,technology,discipline1,discipline1Level,discipline2,discipline2Level,discipline3,discipline3Level,
                   background1,background1Level,background2,background2Level,background3,background3Level,
                   merit1,merit2,flaw1,flaw2,health,willpower,humanity) VALUES (
                   ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                   ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                   ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                   ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                   ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                   ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                   ?, ?)""", request.form["characterName"], session["user_id"], request.form["concept"], request.form["chronicle"],
                   request.form["playerName"],request.form["clan"],request.form["generation"],request.form["strength"],
                   request.form["dexterity"],request.form["stamina"],request.form["charisma"],request.form["manipulation"],
                   request.form["composure"],request.form["intelligence"],request.form["wits"],request.form["resolve"],
                   request.form["athletics"],request.form["brawl"],request.form["craft"],request.form["drive"],
                   request.form["firearms"],request.form["larceny"],request.form["melee"],request.form["stealth"],
                   request.form["survival"],request.form["animalKen"],request.form["etiquette"],request.form["insight"],
                   request.form["intimidation"],request.form["leadership"],request.form["performance"],
                   request.form["persuasion"],request.form["streetwise"],request.form["subterfuge"],request.form["academics"],
                   request.form["awareness"],request.form["finance"],request.form["investigation"],request.form["medicine"],
                   request.form["occult"],request.form["politics"],request.form["science"], request.form["technology"],
                   request.form["discipline1"], request.form["discipline1Level"],request.form["discipline2"],
                   request.form["discipline2Level"], request.form["discipline3"],request.form["discipline3Level"],
                   request.form["background1"], request.form["background1Level"],request.form["background2"],
                   request.form["background2Level"],request.form["background3"], request.form["background3Level"],request.form["merit1"],
                   request.form["merit2"],request.form["flaw1"], request.form["flaw2"],request.form["health"],
                   request.form["willpower"],request.form["humanity"],
                   )
        verify = db.execute("SELECT sheet_id FROM vampire_v5 WHERE characterName = ? AND playerName = ?", request.form["characterName"], request.form["playerName"])
        if not verify:
            return "failure"
        # insert into player_sheets
        db.execute("INSERT INTO player_sheets (user_id, sheet_id, game, characterName) VALUES (?, ?, ?, ?)", session["user_id"], verify[0]["sheet_id"], request.form["game"], request.form["characterName"])
        return redirect(url_for("index"))

@app.route("/delete/", methods=["GET", "POST"])
@login_required
def delete():
        if request.method == "GET":
            query = db.execute("SELECT * FROM player_sheets WHERE user_id = ?", session["user_id"])
            return render_template("delete.html", games=query)
        else:
            sheet = request.form.get("sheet_id")
            if not sheet:
                return "failure, field empty"
            db.execute("DELETE FROM vampire_v5 WHERE sheet_id = ? AND user_id = ?", sheet, session["user_id"])
            db.execute("DELETE FROM player_sheets WHERE sheet_id = ? AND user_id = ?", sheet, session["user_id"])
            flash("deleted from database!")
            return redirect(url_for("delete"))


@app.route("/profile/", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "GET":
        return render_template("profile.html")
    else:
        a = request.form.get("password")
        b = request.form.get("new-password")
        c = request.form.get("confirm-password")
        db_user = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])

        if not a or not b or not c:
            flash("Must fill all fields!", "danger")
            return redirect(url_for("profile"))

        if len(a) < 6 or len(a) > 16 or len(b) < 6 or len(b) > 16 or len(c) < 6 or len(c) > 16:
            flash("Passwords must be between 6 and 16", "danger")
            return redirect(url_for("profile"))

        if not check_password_hash(db_user[0]["hash"], a):
            flash("Wrong password!", "danger" )
            return redirect(url_for("profile"))

        if b != c:
            flash("Passwords don't match", "danger")
            return redirect(url_for("profile"))

        b = generate_password_hash(b)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", b, session["user_id"])
        flash("Done, bro!", "success")
        return redirect(url_for("profile"))



# SUPPORTED_GAMES

# VAMPIRE V5
@app.route("/player/vampire_v5/<sheet_id>/", methods=["GET"])
@login_required
def vampire_v5(sheet_id):
        player_sheet = db.execute("SELECT * FROM vampire_v5 WHERE sheet_id = ?", sheet_id)
        if not player_sheet:
            return "sheet doesn't found"
        else:
            return render_template("/sheets/vamp_v5/vampire_v5.html", data=player_sheet[0])




