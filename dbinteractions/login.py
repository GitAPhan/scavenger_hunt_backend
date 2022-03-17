import datetime
import secrets
from warnings import catch_warnings
import dbinteractions.dbinteractions as c
from flask import Response
import json
import mariadb as db
import helpers.format_response as format


# POST login
def post(user_id, username):
    response = None
    login_id = None
    temp_token = secrets.token_urlsafe(16)

    conn, cursor = c.connect_db()

    try:
        # query request to post login session
        cursor.execute("INSERT INTO login (user_id, login_token) VALUE (?,?)", [user_id, temp_token])
        conn.commit()
        login_id = cursor.lastrowid
        # status check
        if not isinstance(login_id, int):
            response = Response("DB Errror: POST login - no changes were made in the system", mimetype="plain/text", status=400)
    except KeyError:
        response = 'Response'
        # need more exceptions
    
    if response != None:
        return response

    response = {
        "loginId": login_id,
        "userId": user_id,
        "username": username,
        "tempToken": temp_token,
    }
    response_json = json.dumps(response, default=str)
    return Response(response_json, mimetype="application/json", status=201)

def patch(game_id, username, user_id, temp_token, login_id, game_name, game_token, is_owner=False):
    response = None
    login_token = secrets.token_urlsafe(64)
    token = secrets.token_urlsafe(50)

    # query builder
    if is_owner:
        query_keyname = 'master_token'
    else:
        query_keyname = 'player_token'
    query_statement = f"UPDATE login SET game_id=?, login_token=?, {query_keyname}=? WHERE user_id=? AND id=? AND login_token=?"
    
    conn, cursor = c.connect_db()

    try:
        # query to update login session
        cursor.execute(query_statement,[game_id, login_token, token, user_id, login_id, temp_token])
        conn.commit()
        status = cursor.rowcount
        # status check
        if status != 1:
            response = Response('DB Error: PATCH login - no changes were made in the system', mimetype="plain/text", status=400)
    except KeyError:
        response = "Response"
        # need more exceptions

    c.disconnect_db(conn, cursor)

    if response != None:
        return response
    
    # token choice
    token_type ={
        'player_token': "playerToken",
        'master_token': "masterToken"
    }

    response = {
        "gameToken": game_token,
        "loginToken": login_token,
        token_type[query_keyname]: token,
        "gameName": game_name,
        "username": username,        
    }
    response_json = json.dumps(response, default=str)
    response = Response(response_json, mimetype='application/json', status=200)

    # None check - catch
    if response == None:
        response = Response('DbError: PATCH login - catch', mimetype='plain/text', status=499)
    return response
