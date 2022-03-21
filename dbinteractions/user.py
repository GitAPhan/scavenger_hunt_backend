import datetime
import dbinteractions.dbinteractions as c
from flask import Response
import json
import mariadb as db
import helpers.format_response as format
import dbinteractions.login as login


# GET specific user's profile from database
def get(user_id):
    response = None
    user = None

    conn, cursor = c.connect_db()

    try:
        # query to select from database
        cursor.execute(
            "SELECT id, username, name, email FROM user WHERE id=?",
            [user_id],
        )
        user = cursor.fetchall()
        if type(user) is not list:
            response = Response('DbError: GET user - no profile matched the user_id')
    except Exception as e:
        response = Response('DbError: GET user - '+str(e), mimetype="plain/text", status=490)
            # NEED EXCEPTIONS
        print(e)

    c.disconnect_db(conn, cursor)

    if response != None:
        return response

    if user != None:
        response = {
            "userId": user[0][0],
            "username": user[0][1],
            "name": user[0][2],
            "email": user[0][3]
        }

    if response == None:
        response = Response("DB Error: GET user - catch", mimetype="plain/text", status=499)

    return response


# POST user to database
def post(username, password, salt, email, is_over_13, name=None):
    response = None
    user_id = None

    conn, cursor = c.connect_db()

    try:
        # query to create new user
        cursor.execute(
            "INSERT INTO user (username, password, salt, email, is_over_13, name) VALUE (?,?,?,?,?,?)",
            [username, password, salt, email, is_over_13, name],
        )
        conn.commit()
        user_id = cursor.lastrowid
    except db.DatabaseError as DE:
        response = Response('de'+str(DE), mimetype='plain/text', status=400)
    except db.IntegrityError as IE:
        response = Response('ie'+str(IE), mimetype='plain/text', status=400)
    # except Exception as E:
    #         # NEED EXCEPTIONS
    #     print(E)
    #     print(is_over_13)

    c.disconnect_db(conn, cursor)

    if response != None:
        return response

    return login.post(user_id, username)


# PATCH user from database
def patch(user_id, username=None, email=None, birthdate=None, name=None):
    response = None

    # query_request builder
    query_keyname = ""
    query_keyvalue = []
    if username != None:
        query_keyname += " username=?,"
        query_keyvalue.append(username)
    if email != None:
        query_keyname += " email=?,"
        query_keyvalue.append(email)
    if birthdate != None:
        query_keyname += " birthdate=?"
        query_keyvalue.append(birthdate)
    if name != None:
        query_keyname += " name=?"
        query_keyvalue.append(name)
    query_keyvalue.append(user_id)
    query_statement = f"UPDATE user SET{{query_keyname}} WHERE id=?"

    conn, cursor = c.connect_db()

    try:
        # query to edit user
        cursor.execute(query_statement, query_keyname)
        conn.commit()
        status = cursor.commit()
        # status check
        if status != 1:
            response = Response(
                "DB Error: PATCH user - no changes were made in the database",
                mimetype="plain/text",
                status=400,
            )
    except KeyError:
            # NEED EXCEPTIONS
        response = Response("bad bad bad", mimetype="plain/text", status=499)

    # return any value for response that is not None
    if response != None:
        return response

    # grab user info from database to return
    return get(user_id)


# DELETE user from database
def delete(user_id):
    response = None

    conn, cursor = c.connect_db()

    try:
        # query to delete user from database
        cursor.execute("DELETE FROM user WHERE id=?", [user_id])
        conn.commit()
        status = cursor.rowcount
        # status check
        if status != 1:
            response = Response(
                "DB Error: DELETE user - no changes were made in the database",
                mimetype="plain/text",
                status=400,
            )
    except KeyError:
            # NEED EXCEPTIONS
        response = Response("BAD BAD BAD", mimetype="plain/text", status=499)

    c.disconnect_db(conn, cursor)

    # return any value for response that is not None
    if response != None:
        return response

    return Response(
        "user has been successfully deleted", mimetype="plain/text", status=200
    )

# GET username - check availability
def check(username):
    response = None

    conn, cursor = c.connect_db()

    try:
        # query to grab username
        cursor.execute("SELECT COUNT(id) FROM user WHERE username = ?", [username])
        status = cursor.fetchone()[0]
        if status != 0:
            response = Response('username is not available', mimetype='plain/text', status=400)
    except KeyError:
        response = 'Response'
    
    c.disconnect_db(conn, cursor)

    if response != None:
        return response
    
    return Response("username is available", mimetype='plain/text', status=200)
