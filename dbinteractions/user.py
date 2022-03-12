import datetime
import dbinteractions.dbinteractions as c
from flask import Response
import json
import mariadb as db
import helpers.format_response as format


# GET user from database
def get(user_id):
    response = None
    users = None

    conn, cursor = c.connect_db()

    try:
        # query to select from database
        cursor.execute(
            "SELECT id, username, name, email, birthdate, created_at FROM user WHERE user_id=?",
            [user_id],
        )
        users = cursor.fetchall()
    except Exception as e:
        print(e)

    c.disconnect_db(conn, cursor)

    if users != None:
        response = []
        # format response
        for user in users:
            x = format.user(user)
            response.append(x)
        response_json = json.dumps(response, default=str)
        response = Response(response_json, mimetype="application/json", status=200)

    if response == None:
        response = Response(
            "DB Error: GET user - catch", mimetype="plain/text", status=499
        )

    return response


# POST user to database
def post(username, password, salt, email, birthdate, name=None):
    response = None
    user_id = None

    conn, cursor = c.connect_db()

    try:
        # query to create new user
        cursor.execute(
            "INSERT INTO user (username, password, salt, email, birthdate, name) VALUE (?,?,?,?,?,?)",
            [username, password, salt, email, birthdate, name],
        )
        conn.commit()
        user_id = cursor.lastrowid
    except Exception as E:
        print(E)

    c.disconnect_db(conn, cursor)

    if user_id != None:
        # format response
        response = format.user(
            [user_id, username, name, email, birthdate, datetime.datetime.now()]
        )
        response_json = json.dumps(response, default=str)
        response = Response(response_json, mimetype="application/json", status=201)

    # None check - catch
    if response == None:
        response = Response(
            "DB Error: POST user - catch", mimetype="plain/text", status=499
        )

    return response


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
        response = Response("BAD BAD BAD", mimetype="plain/text", status=499)

    c.disconnect_db(conn, cursor)

    # return any value for response that is not None
    if response != None:
        return response

    return Response(
        "user has been successfully deleted", mimetype="plain/text", status=200
    )
