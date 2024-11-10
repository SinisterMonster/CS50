import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Get user data from DB
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])
    user_cash = float(user_cash[0]["cash"])
    user_portfolio = db.execute(
        "SELECT symbol, SUM(shares) AS shares, price FROM transactions WHERE user_id = ? GROUP BY symbol;", session["user_id"])

    # Update stock values
    net_worth = 0

    for stock in user_portfolio:
        stock_data = lookup(stock["symbol"])
        stock["current_stock_price"] = stock_data["price"]
        stock["current_value"] = stock["current_stock_price"] * stock["shares"]
        net_worth += stock["current_value"]

    # Get net worth
    user_net_worth = net_worth + user_cash

    return render_template("index.html", user_portfolio=user_portfolio, user_cash=usd(user_cash), user_net_worth=usd(user_net_worth))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

    # Validate user i/p
        quote = lookup(symbol)

        if not symbol or not quote:
            return apology("Invalid Symbol", 400)
        if not shares or not shares.isnumeric():
            return apology("Invalid shares amount", 400)
        try:
            shares = int(shares)
            if shares < 0:
                return apology("Invalid shares amount", 400)
        except:
            return apology("Invalid (fractional) shares amount", 400)

        # Caluclating costs, keeping track of purchases and user balance in DB
        purchase_cost = shares*quote["price"]
        user_bank_balance = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        if user_bank_balance[0]["cash"] < purchase_cost:
            return apology("Insufficient balance", 400)
        else:
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?,?,?,?,?);",
                       session["user_id"], quote["symbol"], shares, quote["price"], datetime.datetime.now())
            db.execute("UPDATE users SET cash = ? WHERE id = ?;",
                       user_bank_balance[0]["cash"] - purchase_cost, session["user_id"])
            flash("Purchase successful!")
            return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?;", session["user_id"])

    return render_template("history.html", transactions=transactions)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
        symbol = request.form.get("symbol")

        # Get stock info and validate
        quote = lookup(symbol)

        if not quote:
            return apology("Invalid Symbol", 400)
        else:
            return render_template("quoted.html", name=quote["name"], symbol=quote["symbol"], price=quote["price"])

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    session.clear()

    """Register user"""
    if request.method == "POST":

        # Get submission
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate user entries
        if confirmation != password:
            return apology("Passwords dont match", 400)
        if not username:
            return apology("No userrname provided", 400)
        if not password:
            return apology("No password provided", 400)

        # Check DB for username and show error if it exists
        try:
            logged_in_user = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?);", username, generate_password_hash(password))
        except:
            return apology("Duplicate entry: Username already exists", 400)

        # Remember which user has logged in
        session["user_id"] = logged_in_user
        # Send user to homepage
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        sell_symbol = request.form.get("symbol")
        sell_shares = int(request.form.get("shares"))

        # Get quote
        quote = lookup(sell_symbol)

        # Validation #1: Basic validation of user i/p
        if not sell_symbol or not quote["symbol"]:
            return apology("Invalid Symbol", 400)

        if sell_shares < 0 or not sell_shares:
            return apology("Invalid shares amount", 400)

        # Validation #2: Check if user has any or enough shares to sell
        user_portfolio = db.execute(
            "SELECT symbol, SUM(shares) AS total_shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol HAVING total_shares > 0;", session["user_id"], sell_symbol)

        if not user_portfolio or (user_portfolio[0]["total_shares"] < sell_shares):
            return apology("You do not own this stock or you dont own enough of it", 400)
        else:
            # Get user cash in account
            user_cash_account = db.execute(
                "SELECT cash FROM users WHERE id = ?;", session["user_id"])
            user_cash_account = user_cash_account[0]["cash"]

            # Execute sell order->Update trransactions table, update account cash
            db.execute("UPDATE users SET cash = ? WHERE id = ?;",
                       user_cash_account + quote["price"] * sell_shares, session["user_id"])
            db.execute("INSERT INTO transactions (user_id, shares, symbol, price, date) VALUES (?, ?, ?, ?, ?) ;",
                       session["user_id"], -sell_shares, quote["symbol"], quote["price"] * sell_shares, datetime.datetime.now())

            flash("Sale successful!")
            return redirect("/")

    else:
        portfolio = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0;", session["user_id"])
        return render_template("sell.html", portfolio=portfolio)


@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    """Add cash to account"""
    if request.method == "POST":
        amount = float(request.form.get("amount"))

        # Validation
        if not amount or amount < 0:
            return apology("Invalid amount", 400)
        else:
            # Get user account balance
            acount_balance = db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])
            acount_balance = acount_balance[0]["cash"]

            # Set new balance
            db.execute("UPDATE users SET cash = ? WHERE id = ?;",
                       acount_balance + amount, session["user_id"])
            flash("Added cash to account!")
            return redirect("/")

    else:
        return render_template("addcash.html")
