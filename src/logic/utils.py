import os

def getUserName():
    try:
        name = os.getlogin()
    except:
        name = "User"
    return name.capitalize()
