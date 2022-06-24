import dbinteractions.dbinteractions as c
from flask import Response
import json
import mariadb as db

# GET info on all unfinished checkpoints
def get_checkpoint_status(user_id):
    response = None
    open_checkpoints = []

    #get all checkpoints associated with user
    conn, cursor = c.connect_db()

    try:
        cursor.execute("SELECT DISTINCT checkpoint_id from check_in where user_id=?",[user_id])
        checkpoints = cursor.fetchall()
        if checkpoints == []:
            response = Response("no checkpoints are associated with user_id", mimetype='plain/text', status=204)
    except Exception as E:
        response = Response("DbError: get_checkpoint_status - "+str(E), mimetype='plain/text', status=480)

    if response == None:
        try:
            for checkpoint in checkpoints:
                cursor.execute("SELECT IF(COUNT(ci.id)=c.rounds, 'done', c.check_token) from check_in ci inner join checkpoint c on c.id = ci.checkpoint_id where c.id=? and ci.user_id=?", [checkpoint[0], user_id])
                status = cursor.fetchone()
                # grab checkpoint info if game is still open
                if status[0] != 'done': 
                    open_checkpoints.append(status[0])
        except Exception as E:
            response = Response("DbError: get_checkpoint_status - "+str(E), mimetype='plain/text', status=480)

    c.disconnect_db(conn, cursor)

    if response != None:
        return response

    # return open_checkpoints
    open_checkpoints_json = json.dumps(open_checkpoints, default=str)
    return Response(open_checkpoints_json, mimetype='application/json', status=200)

# print(get_checkpoint_status(16)) 
            

# GET checkpoint info from database
def get(game_token=None, checkpoint_id=None, check_token=None):
    response = None
    checkpoints = None

    # query builder
    if game_token != None and checkpoint_id == None and check_token == None:
        keyname = "game_id=(SELECT id FROM game WHERE game_token=?)"
        keyvalue = game_token
    elif check_token != None and game_token == None and checkpoint_id == None:
        keyname = "check_token=?"
        keyvalue = check_token
    elif checkpoint_id != None and game_token == None and check_token == None:
        keyname = "id=?"
        keyvalue = checkpoint_id
    else:
        return Response(
            "you must only choose one argument", mimetype="plain/text", status=400
        )

    query = (f"SELECT id, token_reward, point_reward, rounds, game_type, name FROM checkpoint WHERE {keyname}")

    conn, cursor = c.connect_db()

    try:
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
        # return object if check_token is present
        if check_token != None or checkpoint_id != None:
            return response[0]
        response_json = json.dumps(response, default=str)
        response = Response(response_json, mimetype="application/json", status=200)
    
    if response == None:
        response = Response("DbError: GET checkpoint - catch", mimetype="plain/text", status=499)
    
    return response

# create checkpoints (only GM has permission)
def post():
    response = None

    key = ['masterToken', 'gameToken', 'checkpoint'] #checkpoint will be an array of objects
    