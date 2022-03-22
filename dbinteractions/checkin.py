from select import select
import dbinteractions.dbinteractions as c
from flask import Response
import json
import mariadb as db
import dbinteractions.checkpoint as checkpoint
import dbinteractions.game as game


# is game active check
def is_active(user_id, check_token=None, checkpoint_id=None):
    response = None
    status = None

    # query builder
    if check_token != None:
        keyname = "check_token"
        keyvalue = [user_id, check_token]
    elif checkpoint_id != None:
        keyname = "id"
        keyvalue = [user_id, checkpoint_id]
    query = f"select if(p.rounds=count(c.id), 0, 1) from check_in c inner join checkpoint p on p.id = c.checkpoint_id where c.user_id=? and p.{keyname}=?"

    conn, cursor = c.connect_db()

    try:
        # query
        cursor.execute(query, keyvalue)
        status = cursor.fetchone()
        if status[0] != 1:
            response = False
    except Exception as E:
        response = False
        print(
            "------------------------DB ERROR: CHECK-IN IS_ACTIVE----------------------------"
        )

    c.disconnect_db(conn, cursor)

    if response != None:
        return response
    return True


def get_score(user_id, check_token=None, checkpoint_id=None):
    response = None
    score = None

    # query builder
    if check_token != None:
        keyname = "check_token"
        keyvalue = check_token
    elif checkpoint_id != None:
        keyname = "id"
        keyvalue = checkpoint_id
    else:
        return Response("you must include either the checkpointId or checkToken in request", mimetype="plain/text", status=400)

    query = f"SELECT (SELECT COUNT(c.id) FROM check_in c INNER JOIN checkpoint p ON p.id=c.checkpoint_id WHERE c.user_id=? AND p.{keyname}=?), COUNT(c.id), IFNULL(sum(p.token_reward), 0), IFNULL(sum(p.point_reward),0) FROM check_in c INNER JOIN checkpoint p ON p.id = c.checkpoint_id WHERE c.user_id=? AND p.{keyname}=? AND c.is_winner=1"

    conn, cursor = c.connect_db()

    try:
        # query
        cursor.execute(query, [user_id, keyvalue, user_id, keyvalue])
        score = cursor.fetchall()
        if score == []:
            response = Response(
                "DbError: GET_SCORE check-in - nothing was returned",
                mimetype="plain/text",
                status=204,
            )
    except Exception as E:
        response = Response(
            "DbError: GET_SCORE check-in - " + str(E), mimetype="plain/text", status=490
        )

    c.disconnect_db(conn, cursor)

    if response != None:
        return response

    if score != None:
        response = {
            "roundsPlayed": score[0][0],
            "roundsWon": score[0][1],
            "tokensWon": int(score[0][2]),
            "pointsWon": int(score[0][3]),
        }
        if is_active(user_id, check_token, checkpoint_id):
            response["isActive"] = 1
        else:
            response["isActive"] = 0

    if response == None:
        response = Response(
            "DbError: GET_SCORE check-in - catch", mimetype="plain/text", status=490
        )

    return response


# GET checkpoint_id of specific user
def get_log(user_id):
    response = None
    checkId = None
    logs = None

    conn, cursor = c.connect_db()

    try:
        # query to get distinct checkpoint_id
        cursor.execute(
            "SELECT DISTINCT checkpoint_id FROM check_in WHERE user_id=?", [user_id]
        )
        checkId = cursor.fetchall()
        if checkId == []:
            response = Response(
                "you don't have any checkin entries",
                mimetype="plain/text",
                status=204,
            )
    except KeyError:
        response = "response"
        # need exceptions here

    c.disconnect_db(conn, cursor)

    if response != None:
        return response

    if checkId != None:
        logs = []
        for i in range(0, len(checkId)):
            if not is_active(user_id, checkpoint_id=checkId[i][0]):
                data = checkpoint.get(checkpoint_id=checkId[i][0])
                if type(data) is not dict:
                    return data
                score = get_score(user_id, checkpoint_id=checkId[i][0])
                if type(score) is not dict:
                    return score
                log = data | score
                logs.append(log)
        return Response(
            json.dumps(logs, default=str), mimetype="application/json", status=200
        )
    return Response(
        "DbError: GET_LOG checkin - catch", mimetype="plain/text", status=490
    )


# GET standing
def get_standing(game_token):
    response = None
    players = None

    user_ids = game.get_player(game_token)
    if type(user_ids) is not list:
        return user_ids

    conn, cursor = c.connect_db()

    try:
        players = []
        for user_id in user_ids:
            # query to select all user_id of players
            cursor.execute('select u.id, u.username, ifnull(sum(c.point_reward), 0) from `user` u inner join check_in ci on ci.user_id = u.id inner join checkpoint c on c.id = ci.checkpoint_id where ci.user_id=?', [user_id])
            player = cursor.fetchall()
            if player == []:
                response = Response('error grabbing player standing for user_id '+str(user_id), mimetype="plain/text", status=490)
                raise c.NothingToReturn
            players.append(player[0])
    except c.NothingToReturn:
        pass

    c.disconnect_db(conn, cursor)

    if response != None:
        return response

    response = []
    def find_score(players):
        return players[2]
    players = sorted(players, key=find_score, reverse=True)
    i = 0
    for player in players:
        i += 1
        card = {
            "standing": i,
            "userId": player[0],
            "username": player[1],
            "score": player[2], 
        }
        response.append(card)
    return Response(json.dumps(response, default=str), mimetype="plain/text", status=200)
    

# POST challenge results
def post(game_id, check_token, user_id, result):
    response = None

    conn, cursor = c.connect_db()

    try:
        # insert challenge result into table
        cursor.execute(
            "INSERT INTO check_in (game_id, checkpoint_id, user_id, is_winner) VALUE (?,(SELECT id FROM checkpoint WHERE check_token=?),?,?)",
            [game_id, check_token, user_id, result["isWin"]],
        )
        conn.commit()
        check_id = cursor.lastrowid
        if not isinstance(check_id, int):
            response = Response(
                "DbError: POST check-in - no changes were made",
                mimetype="plain/text",
                status=400,
            )
    except KeyError:
        response = "Response"
        # need exceptions here

    c.disconnect_db(conn, cursor)

    if response != None:
        return response

    data = checkpoint.get(check_token=check_token)
    if type(data) is not dict:
        return data
    score = get_score(user_id, check_token)
    if type(score) is not dict:
        return score
    response = data | score
    response["lastRound"] = result

    return Response(json.dumps(response, default=str), mimetype="application/json", status=200)