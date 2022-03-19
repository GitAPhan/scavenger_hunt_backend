import dbinteractions.dbinteractions as c
from flask import Response
import json
import mariadb as db


# GET checkpoint info from database
def get(game_id=None, checkpoint_id=None, check_token=None):
    response = None
    checkpoints = None

    # query builder
    if game_id != None and checkpoint_id == None and check_token == None:
        keyname = "game_id"
        keyvalue = game_id
    elif check_token != None and game_id == None and checkpoint_id == None:
        keyname = "check_token"
        keyvalue = check_token
    elif checkpoint_id != None and game_id == None and check_token == None:
        keyname = "checkpoint_id"
        keyvalue = checkpoint_id
    else:
        return Response(
            "you must only choose one argument", mimetype="plain/text", status=400
        )

    query = (f"SELECT id, token_reward, point_reward, rounds, game_type, name FROM checkpoint WHERE {keyname} =?")

    conn, cursor = c.connect_db()

    try:
        print(query)
        cursor.execute(query, [keyvalue])
        checkpoints = cursor.fetchall()
        if checkpoints == []:
            response = Response("nothing to return", mimetype="plain/text", status=204)
    except KeyError:
        response = "Response"
    except Exception as E:
        response = Response("DbError: GET checkpoint - exception catch"+str(E), mimetype="plain/text", status=480)

    # need more exceptions

    c.disconnect_db(conn, cursor)

    if response != None:
        return response

    # prepare response package
    if checkpoints != None:
        response = []
        key = [
            "checkpointId",
            "tokenReward",
            "pointReward",
            "rounds",
            "gameType",
            "gameName",
        ]
        for checkpoint in checkpoints:
            set = {}
            for i in range(0,len(checkpoint)):
                set[key[i]] = checkpoint[i]
            response.append(set)
        response_json = json.dumps(response, default=str)
        response = Response(response_json, mimetype="application/json", status=200)
    
    if response == None:
        response = Response("DbError: GET checkpoint - catch", mimetype="plain/text", status=499)
    
    return response