import os

from datetime import datetime
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, search_tv_show, get_tv_show_details, omDetails
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def insert_user(username, hash_value):
    con = sqlite3.connect("tenet.db")
    db = con.cursor()
    db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash_value))
    con.commit()
    con.close()


def checklogin(username):
    con = sqlite3.connect("tenet.db")
    db = con.cursor()
    db.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = db.fetchone()
    con.commit()
    con.close()
    return row


def matchingupdb():
    con = sqlite3.connect("tenet.db")
    db = con.cursor()
    db.execute("select * from matchingup where user_id = ?",(session["user_id"],))
    matchupsDraft = db.fetchall()
    con.commit()
    con.close()
    return matchupsDraft

from datetime import datetime, timedelta

from datetime import datetime


def pluralize(value, unit):
    return f"{value} {unit}{'' if value == 1 else 's'} ago"


def time_ago(post_time_str):
    # Convert ISO string to datetime
    post_time = datetime.fromisoformat(post_time_str)
    now = datetime.now()
    diff = now - post_time

    seconds = int(diff.total_seconds())
    minutes = seconds // 60
    hours = minutes // 60
    days = diff.days
    weeks = days // 7
    months = days // 30
    years = days // 365

    if seconds < 60:
        return pluralize(seconds, "second")
    elif minutes < 60:
        return pluralize(minutes, "minute")
    elif hours < 24:
        return pluralize(hours, "hour")
    elif days < 7:
        return pluralize(days, "day")
    elif weeks < 4:
        return pluralize(weeks, "week")
    elif months < 12:
        return pluralize(months, "month")
    else:
        return pluralize(years, "year")


def first_nouse():
    con = sqlite3.connect("tenet.db")
    db = con.cursor()
    db.execute("select * from matchingup where user_id = ?",(session["user_id"],))
    matchupsDraft = db.fetchone()
    con.commit()
    con.close()
    return False if matchupsDraft else True


def add_comment(comment, uid, matid):
    if comment:
        now = datetime.now().isoformat()
        con = sqlite3.connect("tenet.db")
        con.row_factory = sqlite3.Row
        db = con.cursor()
        db.execute("select username from users where id = ?",(uid,))
        row = db.fetchone()
        db.execute("""
                        INSERT INTO comments (user_id, matchup_id, comment, timestamp, username)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        uid,
                        matid,
                        comment,
                        now,
                        row["username"]
                    ))
        con.commit()
        con.close()
        return
    else:
        return


def addtomatchup(tmdb_id):
    details = get_tv_show_details(tmdb_id)
    if details:
        omdb = omDetails(details['external_ids']['imdb_id'])
        con = sqlite3.connect("tenet.db")
        db = con.cursor()

        imdb_id = details.get("external_ids", {}).get("imdb_id")
        tvdb_id = details.get("external_ids", {}).get("tvdb_id")

        
        db.execute("select id from shows where tmdb_id = ?", (tmdb_id,))
        istm = db.fetchone()
        if istm:
            show_id = istm[0]
        else:
            if omdb:
                if details["poster_path"]:
                    poster = f"https://image.tmdb.org/t/p/w300{details["poster_path"]}"
                else:
                    poster = None
                db.execute("""
                    INSERT INTO shows (title, release_date, genre, tmdb_id, imdb_id, tvdb_id, posters)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    details.get('name'),
                    details.get('first_air_date')[:4] if details.get('first_air_date') else None,
                    omdb.get('Genre'),
                    tmdb_id,
                    imdb_id,
                    tvdb_id,
                    poster
                ))
                con.commit()

                db.execute("select id from shows where tmdb_id = ?", (tmdb_id,))
                show_id = db.fetchone()[0]
            else:
                return apology ("error getting om show details")

        db.execute("SELECT * FROM matchingup WHERE user_id = ?", (session["user_id"],))
        first = db.fetchone()
        
        now = datetime.now().isoformat()

        if not first:
            db.execute("""
                INSERT INTO matchingup (user_id, show1_id, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, (session["user_id"], show_id, now, now))

        else:
            db.execute("""
                UPDATE matchingup
                SET show2_id = ?, updated_at = ?
                WHERE user_id = ?
            """, (show_id, now, session["user_id"]))
            con.commit()

            db.execute("""
                INSERT INTO matchups (show1_id, show2_id, person_id, timestamp)
                SELECT show1_id, show2_id, user_id, ?
                FROM matchingup
                WHERE user_id = ?
            """, (datetime.now().isoformat(), session["user_id"]))

            db.execute("DELETE FROM matchingup WHERE user_id = ?", (session["user_id"],))
            
        con.commit()
        con.close()
        return
    else:
        return apology("error geting show details")


def getMatchup(matchupID):
    con = sqlite3.connect("tenet.db")
    con.row_factory = sqlite3.Row
    db = con.cursor()
    db.execute("select * from matchups where id = ?",(matchupID,))
    result = db.fetchone()
    con.commit()
    con.close()
    return result


def get_tmdb(show_id):
    con = sqlite3.connect("tenet.db")
    db = con.cursor()
    db.execute("select tmdb_id from shows where id = ?",(show_id,))
    result = db.fetchone()
    con.commit()
    con.close()
    return result[0]

def get_all_match():
    con = sqlite3.connect("tenet.db")
    con.row_factory = sqlite3.Row
    db = con.cursor()
    db.execute("SELECT * FROM matchups ORDER BY timestamp DESC LIMIT 20")
    rows = db.fetchall()
    con.commit()
    con.close()
    return rows


def get_from_shows(id):
    con = sqlite3.connect("tenet.db")
    con.row_factory = sqlite3.Row
    db = con.cursor()
    db.execute("SELECT * FROM shows where id = ?",(id,))
    rows = db.fetchone()
    con.commit()
    con.close()
    return rows


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    matchups = get_all_match()
    abc = []
    liked = []
    beforelikes = []
    # show1sid = []
    # show2sid = []
    ids = []
    namesa = []
    namesb = []
    postersa = []
    postersb = []
    for match in matchups:
        show1 = get_from_shows(match["show1_id"])
        show2 = get_from_shows(match["show2_id"])

        # show1sid.append(match["show1_id"])
        # show2sid.append(match["show2_id"])
        try:
            con = sqlite3.connect("tenet.db")
            con.row_factory = sqlite3.Row
            db = con.cursor()
            db.execute("select voted_for_show_id from votes where matchup_id = ? and voter_id = ?",(match["id"], session["user_id"]))
            row = db.fetchone()
            con.close()
        except:
            row = []

        if row:
            liked.append(1)
            if row["voted_for_show_id"] == match["show1_id"]:
                abc.append(1)
            else:
                abc.append(2)
        else:
            liked.append(0)

        if show1 and show2:
            postersa.append(show1["posters"])
            postersb.append(show2["posters"])
            namesa.append(show1["title"])
            namesb.append(show2["title"])
        else:
            return apology("error getting show details")

        ids.append(match["id"])
        con = sqlite3.connect("tenet.db")
        db = con.cursor()
        db.execute("SELECT COUNT(*) FROM votes WHERE matchup_id = ? AND voted_for_show_id = ?", (match["id"],match["show1_id"]))
        likefor1 = db.fetchone()
        db.execute("SELECT COUNT(*) FROM votes WHERE matchup_id = ? AND voted_for_show_id = ?", (match["id"],match["show2_id"]))
        likefor2 = db.fetchone()
        con.close()

        beforelikes.append([likefor1[0],likefor2[0]])

    return render_template("index.html", postersa = postersa, namesa = namesa, ids = ids, postersb = postersb, namesb = namesb, liked = liked, abc = abc, beforelikes = beforelikes)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirm password does not match", 400)

        username = request.form.get("username")
        hash = generate_password_hash(request.form.get("password"))

        try:
            con = sqlite3.connect("tenet.db")
            db = con.cursor()
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash))
            con.commit()
            con.close()
            return redirect("/")
        except sqlite3.IntegrityError:
            return apology("username already exist", 400)
            
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        
        # Query database for username
        row = checklogin(request.form.get("username"))

        
        # Ensure username exists and password is correct
        if not row or not check_password_hash(
            row[2], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = row[0]

        # Redirect user to home page
        return redirect("/")
        

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route('/search',methods = ["GET", "POST"])
def search():
    query = request.args.get('query')
    if not query:
        return redirect("/")
    
    results = search_tv_show(query)

    if request.method == "POST":
        return jsonify(results)
    else:
        return render_template("searched.html", results = results)


@app.route('/details/<int:show_id>',methods = ['GET','POST'])
@login_required
def details(show_id):
    details = get_tv_show_details(show_id)
    
    # Optional: Check if the result is valid
    if request.method == 'GET':

        if "status_code" in details and details["status_code"] == 34:
            details = None

        '''return jsonify(details)'''
        if details:
            ttid = details["external_ids"]["imdb_id"]
            poster = f"https://image.tmdb.org/t/p/w300{details["poster_path"]}"
            omdb = omDetails(ttid)
            if omdb:
                return render_template("details.html", details = details, poster = poster, omdb = omdb)
            else:
                return apology("error getting om show details")
        else:
            return apology("error getting show details")
    else:
        addtomatchup(show_id)
        return redirect("/")


@app.route('/matchup/comments/<int:matchupID>',methods = ['GET','POST'])
@login_required
def matchup(matchupID):
    if request.method == 'GET':
        matchups = getMatchup(matchupID)
        if not matchup:
            return apology("Matchup not found", 404)
        

        con = sqlite3.connect("tenet.db")
        con.row_factory = sqlite3.Row
        db = con.cursor()

        db.execute("SELECT show1_id, show2_id FROM matchups WHERE id = ?", (matchupID,))
        showids = db.fetchone()

        if showids:
            show1D = get_from_shows(showids["show1_id"])
            show2D = get_from_shows(showids["show2_id"])
        else:
            show1D = show2D = None

        db.execute('SELECT username, comment, timestamp FROM comments WHERE matchup_id = ? ORDER BY timestamp DESC', (matchupID,))
        comments = db.fetchall()

        con.close()

        ago = []
        for comment in comments:
            ago.append(time_ago(comment["timestamp"]))
        
        if show1D and show2D:
                return render_template("matchup.html", show1 = show1D, show2 = show2D, matchupID=matchupID, comments=comments, time_ago =ago)
        else:
                return apology("error getting show details")
        
    else:
        comment = request.form.get("comment")
        user_id = session["user_id"]
        add_comment(comment, user_id, matchupID)
        return redirect(f"{matchupID}")
    

@app.route('/post/<int:matchup_id>/<likes>', methods=['GET', 'POST'])
@login_required
def handle_like(matchup_id, likes):
    if likes not in ['like1', 'like2']:
        return jsonify({'error': 'Invalid rating'}), 400

    userid = session["user_id"]
    now = datetime.now().isoformat()

    con = sqlite3.connect("tenet.db")
    con.row_factory = sqlite3.Row
    db = con.cursor()

    db.execute("SELECT show1_id, show2_id FROM matchups WHERE id = ?", (matchup_id,))
    showids = db.fetchone()

    if not showids:
        con.close()
        return jsonify({'error': 'Matchup not found'}), 404

    target_id = showids['show1_id'] if likes == "like1" else showids['show2_id']

    db.execute("SELECT voted_for_show_id FROM votes WHERE matchup_id = ? AND voter_id = ?", (matchup_id, userid))
    row = db.fetchone()

    if row:
        if row["voted_for_show_id"] != target_id:
            db.execute("""
                UPDATE votes
                SET voted_for_show_id = ?, timestamp = ?
                WHERE voter_id = ? AND matchup_id = ?
            """, (target_id, now, userid, matchup_id))
    else:
        db.execute("""
            INSERT INTO votes (matchup_id, voted_for_show_id, voter_id, timestamp)
            VALUES (?, ?, ?, ?)
        """, (matchup_id, target_id, userid, now))

    con.commit()
    con.close()
    return jsonify({"success": True})


@app.route('/gtf')
def gtf():
    return render_template("gtf.html")


@app.route('/profile')
def profile():
    return render_template("profile.html")
