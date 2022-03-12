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
        response = Response("BAD BAD BAD", mimetype="plain/text", status=499)

    c.disconnect_db(conn, cursor)

    if game != None:
        response = format.game(game)

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

    if response != None:
        return response

    if game_id != None and game_token != None:
        response = format.game([game_id, name, game_token, user_id])

    if response == None:
        response = Response(
            "DB Error: POST game - catch", mimetype="plain/text", status=499
        )

    return response


# PATCH game to database
def post(game_id, start_time=None, duration=None, name=None):
    response = None
