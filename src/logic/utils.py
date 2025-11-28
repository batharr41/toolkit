import os


def getUserName():
    try:
        name = os.getlogin()
    except:
        name = "User"
    return name.capitalize()


def tryParseInt(no: str, defVal):
    try:
        return int(no)
    except:
        return defVal
