# https://docs.cs50.net/2019/x/psets/8/finance/finance.html
# Implement a website via which users can "buy" and "sell" stocks.

import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    rows = db.execute("SELECT cash FROM users WHERE id = :userid", userid=session['user_id'])
    cash = rows[0]['cash']

    rows = db.execute(
        "SELECT symbol, SUM(movement) AS quantity, company FROM movements WHERE user_id = :user_id GROUP BY symbol HAVING quantity > 0", user_id=session['user_id'])
    movements = []
    total = cash

    for row in rows:
        stock = lookup(row['symbol'])
        movement = row
        movement['unit_value'] = usd(stock['price'])
        total_value_for_share = float(row['quantity']) * float(stock['price'])
        movement['total_value'] = usd(total_value_for_share)
        total = float(total) + total_value_for_share
        movements.append(movement)

    return render_template("index.html", cash=usd(cash), movements=movements, total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        if not request.form.get("shares"):
            return apology("must provide shares", 400)

        try:
            if not float(request.form.get("shares")).is_integer():
                return apology("shares must be a positive integer", 400)
        except ValueError:
            return apology("shares must be a valid number", 400)

        if int(request.form.get("shares")) < 1:
            return apology("shares must be a positive number", 400)

        stock = lookup(request.form.get("symbol"))

        if not stock or not stock['name']:
            return apology("symbol was not found", 400)

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        query = db.execute("SELECT cash FROM users WHERE id = :userid", userid=session['user_id'])
        user_cash = query[0]['cash']

        total_price_for_transaction = float(shares) * float(stock['price'])
        new_cash_for_user = float(user_cash) - float(total_price_for_transaction)

        if new_cash_for_user < 0:
            return apology("you don't have enough money", 400)

        db.execute("INSERT INTO movements (symbol, movement, user_id, unit_value, company) VALUES (:symbol, :movement, :user_id, :unit_value, :company)",
                   symbol=symbol, movement=shares, user_id=session['user_id'], unit_value=stock['price'], company=stock['name'])

        db.execute("UPDATE users SET cash = :new_cash WHERE id=:user_id", new_cash=new_cash_for_user, user_id=session['user_id'])

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    # Ensure username was submitted
    username = request.args.get("username")

    if not username:
        return jsonify(False)
    elif username and len(username) < 1:
        return jsonify(False)

    query = db.execute("SELECT COUNT(*) AS COUNTUSERS FROM users WHERE username = :username", username=username)

    if query[0]['COUNTUSERS'] == 0:
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT cash FROM users WHERE id = :userid", userid=session['user_id'])
    cash = rows[0]['cash']

    rows = db.execute("SELECT * FROM movements WHERE user_id = :userid", userid=session['user_id'])
    movements = []

    for row in rows:
        movement = row
        movement['total_value'] = usd(float(abs(movement['movement']) * movement['unit_value']))
        movement['unit_value'] = usd(movement['unit_value'])
        movements.append(movement)

    return render_template("history.html", cash=usd(cash), movements=movements)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        data = lookup(request.form.get("symbol"))

        if data:
            return render_template("quoted.html", name=data["name"], symbol=data["symbol"], price=usd(data["price"]))
        else:
            return apology("symbol provided was not found", 400)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        # Ensure password and password confirmation match
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Check if username is not already used
        query = db.execute("SELECT COUNT(*) AS COUNTUSERS FROM users WHERE username = :username",
                           username=request.form.get("username"))

        if query[0]['COUNTUSERS'] == 0:
            username = request.form.get("username")
            hashed = generate_password_hash(request.form.get("password"))

            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hashed)", username=username, hashed=hashed)

            return render_template("register.html", success="OK")
        else:
            return apology("username not available", 400)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        if not request.form.get("shares"):
            return apology("must provide shares", 400)
        if request.form.get("shares") and int(request.form.get("shares")) < 1:
            return apology("must provide positive shares", 400)

        shares = int(request.form.get("shares"))
        symbol = request.form.get("symbol")

        stock = lookup(request.form.get("symbol"))

        if not stock or not stock['name']:
            return apology("symbol was not found", 400)

        query = db.execute("SELECT SUM(movement) AS user_shares_count FROM movements WHERE symbol = :symbol AND user_id = :user_id",
                           symbol=symbol, user_id=session["user_id"])

        user_shares_count = int(query[0]['user_shares_count'])

        if user_shares_count < shares:
            return apology("you don't have enough shares for this symbol", 400)

        total_price_for_transaction = float(shares) * float(stock['price'])

        # Set a negative movement
        movement = float(shares*-1)

        db.execute("INSERT INTO movements (symbol, movement, user_id, unit_value, company) VALUES (:symbol, :movement, :user_id, :unit_value, :company)",
                   symbol=symbol, movement=movement, user_id=session['user_id'], unit_value=stock['price'], company=stock['name'])

        db.execute("UPDATE users SET cash = cash + :new_cash WHERE id = :user_id",
                   new_cash=total_price_for_transaction, user_id=session['user_id'])

        return redirect("/")
    else:
        rows = db.execute(
            "SELECT symbol, SUM(movement) AS quantity FROM movements WHERE user_id = :user_id GROUP BY symbol HAVING quantity > 0", user_id=session['user_id'])
        symbols = []

        for row in rows:
            symbols.append(row['symbol'])

        return render_template("sell.html", symbols=symbols)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
