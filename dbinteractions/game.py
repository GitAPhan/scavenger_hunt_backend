import secrets
import mariadb as db
import dbinteractions.dbinteractions as c
import json
from flask import Response
import helpers.format_response as format

# GET game from database
def get(game_id):
    response = None
    game = None

    conn, cursor = c.connect_db()

    try:
        # query to select from database
        cursor.execute(
            "SELECT id, name, game_token, user_id, start_time, duration FROM game where id=?",
            [game_id],
        )
        game = cursor.fetchall()
        status = cursor.rowcount
        # status check
        if isinstance(status, int) == False or status == 0:
            response = Response(
                "Looks like that game isn't real!", mimetype="plain/text", status=404
            )
    except KeyError:
            # NEED EXCEPTIONS
        response = Response("BAD BAD BAD", mimetype="plain/text", status=499)

    c.disconnect_db(conn, cursor)

    # format response
    if game != None:
        response = format.game(game)
        response_json = json.dumps(response, default=str)
        response = Response(response_json, mimetype="application/json", status=200)

    # None check - catch
    if response == None:
        response = Response(
            "DB Error: GET game - catch", mimetype="plain/text", status=499
        )

    return response


# POST game to database
def post(name, user_id, start_time=None, duration="04:00:00"):
    response = None
    game_id = None
    game_token = None

    conn, cursor = c.connect_db()

    while True:
        try:
            game_token = secrets.token_hex(7)
            # query to create a new game
            cursor.execute(
                "INSERT INTO game (game_token, user_id, duration, start_time, name) VALUE (?,?,?,?,?)",
                [game_token, user_id, duration, start_time, name],
            )
            conn.commit()
            game_id = cursor.lastrowid
            # status check
            if isinstance(game_id, int):
                break
        except KeyError:
            response = Response("BAD BAD BAD", mimetype="plain/text", status=499)
            # NEED EXCEPTIONS
            break
        except db.IntegrityError as IE:
            # duplicate game_token
            if "Duplicate" in str(IE) and "game_token" in str(IE):
                pass
            else:
                response = Response(
                    "BAD BAD BAD" + str(IE), mimetype="plain/text", status=499
                )
                break

    c.disconnect_db

    # return any value for response that isn't None
    if response != None:
        return response

    # format response 
    if game_id != None and game_token != None:
        response = format.game([game_id, name, game_token, user_id])
        response_json = json.dumps(response, default=str)
        response = Response(response_json, mimetype="application/json", status=201)

    # None check - catch
    if response == None:
        response = Response(
            "DB Error: POST game - catch", mimetype="plain/text", status=499
        )

    return response


# PATCH game to database
def patch(game_id, start_time=None, duration=None, name=None):
    response = None

    # query request builder
    query_keyname = ""
    query_keyvalue = []
    if name != None:
        query_keyname += "name=?, "
        query_keyvalue.append(name)
    if duration != None:
        query_keyname += "duration=?, "
        query_keyvalue.append(duration)
    if start_time != None:
        query_keyname += "start_time=?, "
        query_keyvalue.append(start_time)
    # all arguments can't be none
    if name == None and duration == None and start_time == None:
        return Response("please enter at least one value (start_time/duration/name)", mimetype="plain/text", status=400)
    query_keyvalue.append(game_id)
    query_statement = f"UPDATE game SET {{query_keyname[0:-2]}} WHERE id=?"

    conn, cursor = c.connect_db()

    try:
        # query request to edit game in database
        cursor.execute(query_statement, query_keyvalue)
        conn.commit()
        status = cursor.rowcount
        # status check
        if status != 1:
            response = Response("DB Error: PATCH game - looks like no changes were made to your game", mimetype="plain/text", status=400)
    except KeyError:
            # NEED EXCEPTIONS
        response = Response("BAD BAD BAD", mimetype="plain/text", status=499)
    
    c.disconnect_db(conn, cursor)

    # return any value in response that isn't none
    if response != None:
        return response
        
    # return updated entry from the database
    return get(game_id)


# DELETE game in database
def delete(game_id, user_id):
    response = None

    conn, cursor = c.connect_db()

    try:
        # query request to delete game in database
        cursor.execute("DELETE FROM game WHERE id=? AND user_id=?")