import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import yfinance as yf

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["cad"] = cad

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Show portfolio of stocks"""

    # Get user data from DB
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])
    user_cash = float(user_cash[0]["cash"])
    user_portfolio = db.execute(
        "SELECT symbol, SUM(shares) AS shares, price FROM transactions WHERE user_id = ? GROUP BY symbol;", session["user_id"])

    # Update stock values
    net_worth = 0

    # Get net worth
    user_net_worth = net_worth + user_cash

    return render_template("index.html", user_portfolio=user_portfolio, user_cash=usd(user_cash), user_net_worth=usd(user_net_worth))
