from cs50 import get_float

# Get non-negetive input from user
while True:
    try:
        # The rounding and *100 seems silly but this is to elimanate issues I was seeing with floating point precision
        cash = round(get_float("Change: "), 2) * 100
        if (cash >= 0):
            break
    except:
        pass

# Some coin variable to make it easier to read
coins = 0
quarter = 25
dime = 10
nickel = 5
penny = 1

# Calculating
while cash > 0:
    if cash >= quarter:
        cash = cash - quarter
        coins += 1
    elif cash >= dime:
        cash = cash - dime
        coins += 1
    elif cash >= nickel:
        cash = cash - nickel
        coins += 1
    else:
        cash = cash - penny
        coins += 1

print(coins)
