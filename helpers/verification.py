import hashlib
import re
import secrets
from flask import Response
import mariadb as db
from dbinteractions.dbinteractions import connect_db, disconnect_db

# verify that the password is not weak
def new_password(password):
    if len(password) < 8:
        return False
    # regex validation: needs to contain upper, lower, numeric, and a special character
    if re.fullmatch(
        r"((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W])(?!.*[\s]).{8,64})", password
    ):
        return True
    else:
        return False


# verify that user input username is valid
def username(username):
    # username cannot contain a whitespace or '@' and between 8-64 characters
    if re.fullmatch(r"(?!.[@\s])([a-zA-Z0-9\-\_\.]{8,64})", username):
        return True
    else:
        return False


# create salt, add to password, hash
def create_password(password):
    salt = secrets.token_urlsafe(10)
    password = password + salt
    hash_result = hashlib.sha512(password.encode()).hexdigest()
    return hash_result, salt


# Grab the hashed salty password and the salt to add to the password, hash and verify
def password(hashed_salty_password, salt, password):
    password = password + salt
    verify_hsp = hashlib.sha512(password.encode()).hexdigest()
    # verify
    if hashed_salty_password == verify_hsp:
        return True
    else:
        return False


# grab hashed_password and salt from database to be verified
def get_hashpass(payload, type):
    conn, cursor = connect_db()
    result = None

    # modify query
    choices = {
        "loginToken": "l.login_token",
        "username": "u.username",
        "email": "u.email",
    }
    query_selector = choices[type]
    # conditional to remove innerjoin if user enters email or username
    query_innerjoin = "inner join login l on l.user_id = u.id"
    if type != "loginToken":
        query_innerjoin = ""
    query_statement = f"select u.password, u.salt, u.id from user u {query_innerjoin} where {query_selector} = ?"

    try:
        cursor.execute(query_statement, [payload])
        result = cursor.fetchone()
    except Exception as E:
        return (
            False,
            Response(
                "DB Auth Error: GET cred -" + str(E),
                mimetype="plain/text",
                status="401",
            ),
            None,
        )

    disconnect_db(conn, cursor)

    if result == None:
        return (
            False,
            Response(
                "Authentication Error - invalid login credentials",
                mimetype="plain/text",
                status=401,
            ),
            None,
        )
    else:
        return result[0], result[1], result[2]


## TOKEN VILLE ##

# verify login token
def loginToken(login_token, login_id, user_id):
    response = None
    status = None

    conn, cursor = connect_db()

    try:
        # query to select row count and verify
        cursor.execute(
            "SELECT COUNT(l.id), u.username FROM login l INNER JOIN user u ON u.id = l.user_id WHERE l.login_token=? AND l.id=? AND l.user_id=?",
            [login_token, login_id, user_id],
        )
        status = cursor.fetchall()[0]
        # status check
        if status[0] != 1:
            response = Response(
                "unauthorized operation", mimetype="plain/text", status=403
            )
    except KeyError:
        response = "response"

    disconnect_db(conn, cursor)

    if response != None:
        return False, response

    if status == None:
        return False, Response(
            "unable to verify login session", mimetype="plain/text", status=403
        )

    # return back verify status and username
    return True, status[1]


# verify gameToken is valid
def gameToken(gameToken):
    response = None
    isValid = None

    conn, cursor = connect_db()

    try:
        # query to select game_id & game_name
        cursor.execute("SELECT id, name FROM game where game_token=?", [gameToken])
        isValid = cursor.fetchall()
        # status check
        if isValid == []:
            response = Response(
                "token is non-existant", mimetype="plain/text", status=404
            )
    except KeyError:
        response = "Response"

    disconnect_db(conn, cursor)

    if response != None:
        return False, response
    if isValid != None:
        # return game_id, game_name
        return isValid[0][0], isValid[0][1]
    # catch
    return False, Response(
        "VerifyError: GAME_TOKEN - catch error", mimetype="plain/text", status=499
    )


# verify that player's login session is valid
def player(playerToken):
    response = None
    isValid = None

    conn, cursor = connect_db()

    try:
        # query to select game_id and user_id from login
        cursor.execute(
            "SELECT game_id, user_id FROM login WHERE player_token=?", [playerToken]
        )
        isValid = cursor.fetchall()
        # status check
        if isValid == []:
            response = Response(
                "player token is not valid", mimetype="plain/text", status=403
            )
    except KeyError:
        response = "response"
        # need exceptions here

    disconnect_db(conn, cursor)

    if response != None:
        return False, response

    if isValid != None:
        return isValid[0][0], isValid[0][1]

    return False, Response("playerToken auth error", mimetype="plain/text", status=499)
