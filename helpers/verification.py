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
    if re.fullmatch(r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W])(?!.*[\s]).{8,64})', password):
        return True
    else:
        return False

# verify that user input username is valid
def username(username):
    # username cannot contain a whitespace or '@' and between 8-64 characters
    if re.fullmatch(r'(?!.[@\s])([a-zA-Z0-9\-\_\.]{8,64})', username):
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

# verify that the loginToken in valid
def loginToken(loginToken):
    conn, cursor = connect_db()
    user = None
    verify_status = None

    try:
        # query to select userId and username of user related to the loginToken
        cursor.execute("SELECT u.id, u.username FROM login l INNER JOIN user u ON u.id = l.user_id WHERE l.login_token = ?", [loginToken])
        response = cursor.fetchall()[0]
        user = {
            'id': response[0],
            'name': response[1]
        }
        
        if isinstance(user["id"], int):
            verify_status = True

    except TypeError:
        user = Response("USER: invalid 'loginToken'", mimetype="plain/text", status=401)
        verify_status = False
    except IndexError:
        user = Response("USER: invalid 'loginToken'", mimetype="plain/text", status=403)
        verify_status = False
    except db.OperationalError as oe:
        user = Response("DB Error: " + str(oe), mimetype="plain/text", status=500)
        verify_status = False
    except Exception as E:
        user = Response("Verify Error: general 'loginToken' error"+str(E), mimetype="plain/text", status=498)
        verify_status = False
    
    disconnect_db(conn,cursor)
    return user, verify_status