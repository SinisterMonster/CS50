from cs50 import get_int

# Get input between 1-8:
while (True):
    try:
        height = get_int("Height: ")
        if (height > 0 and height < 9):
            break
    except:
        pass

# Now print <MARIO MORE>
for i in range(height):
    print(" " * (height - i - 1) + "#" * (i + 1) + "  " + "#" * (i + 1))

# This is <MARIO LESS>\
    #print(" " * (height - i - 1) + "#" * (i + 1))
