import dbinteractions.dbinteractions as c
from flask import Response
import json
import mariadb as db

# GET challenge info
def get(check_token, user_id=None, score=None):
    response = None
    data = None

    # let the crazy query building begin!!
    inner_join = "INNER JOIN check_in c ON c.checkpoint_id = p.id "
    col_roundsPlayed = ", (select count(c.id) from check_in c inner join checkpoint p on p.id=c.checkpoint_id where c.user_id=? and p.check_token=?), "
    col_roundsWon = "(select count(c.id) from check_in c inner join checkpoint p on p.id=c.checkpoint_id where c.is_winner=1 and c.user_id=? and p.check_token=?), "
    col_pointsWon = "(select sum(p.point_reward) from check_in c inner join checkpoint p on p.id = c.checkpoint_id where c.user_id=? and p.check_token=? and c.is_winner=1), "
    col_tokensWon = "(select sum(p.token_reward) from check_in c inner join checkpoint p on p.id = c.checkpoint_id where c.user_id=? and p.check_token=? and c.is_winner=1)"
    col_isActive = ", (select if(p.rounds=count(c.id), 0, 1) from check_in c inner join checkpoint p on p.id = c.checkpoint_id where c.user_id=? and p.check_token=?)"
    user_stats = (
        col_roundsPlayed + col_roundsWon + col_pointsWon + col_tokensWon + col_isActive
    )
    keyname = " AND c.user_id =?"
    keyvalue = [
        user_id,
        check_token,
        user_id,
        check_token,
        user_id,
        check_token,
        user_id,
        check_token,
        user_id,
        check_token,
        check_token,
        user_id,
    ]
    if user_id == None:
        inner_join = ""
        user_stats = ""
        keyname = ""
        keyvalue = [check_token]
    query_statement = f"SELECT p.id, p.token_reward, p.point_reward, p.rounds, p.game_type, p.name{user_stats} FROM checkpoint p {inner_join}WHERE p.check_token=?{keyname}"

    conn, cursor = c.connect_db()

    try:
        # query to select game info(token_reward, point_reward, rounds, game_type) and game status(rounds_played, rounds_won, points_won, tokens_awarded)
        cursor.execute(query_statement, keyvalue)
        data = cursor.fetchall()
        if data == []:
            response = Response(
                "DbError: GET check-in - no entries found",
                mimetype="plain/text",
                status=400,
            )
    except KeyError:
        response = "Response"

    c.disconnect_db(conn, cursor)

    if response != None:
        return response

    response_key = [
        "checkpointId",
        "tokenReward",
        "pointReward",
        "rounds",
        "gameType",
        "gameName",
        "roundsPlayed",
        "roundsWon",
        "pointsWon",
        "tokensWon",
        "isActive",
    ]

    if data != None:
        response = {}
        # if score is present
        if score != None:
            response["lastRound"] = score
        for i in range(0, len(data[0])):
            if data[0][i] == None:
                response[response_key[i]] = 0
            else:
                response[response_key[i]] = data[0][i]
        response_json = json.dumps(response, default=str)
        response = Response(response_json, mimetype="application/json", status=200)

    if response == None:
        response = Response(
            "DbError: GET check-in - catch", mimetype="plain/text", status=499
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
                "no checkpoint_id associated with user_id",
                mimetype="plain/text",
                status=400,
            )
    except KeyError:
        response = "response"
        # need exceptions here

    c.disconnect_db(conn, cursor)

    if response != None:
        return response

    if checkId == None:
        return Response(
            "something went wrong!! GET LOG", mimetype="plain/text", status=499
        )
    inner_join = "INNER JOIN check_in ci ON ci.checkpoint_id = c.id "
    col_roundsPlayed = ", (select count(id) from check_in where user_id=? and checkpoint_id=?), "
    col_roundsWon = "(select count(id) from check_in where is_winner=1 and user_id=? and checkpoint_id=?), "
    col_pointsWon = "(select sum(c.point_reward) from check_in ci inner join checkpoint c on c.id = ci.checkpoint_id where ci.user_id=? and ci.checkpoint_id=? and ci.is_winner=1), "
    col_tokensWon = "(select sum(c.token_reward) from check_in ci inner join checkpoint c on c.id = ci.checkpoint_id where ci.user_id=? and ci.checkpoint_id=? and ci.is_winner=1)"
    col_isActive = ", (select if(c.rounds=count(ci.id), 0, 1) from check_in ci inner join checkpoint c on c.id = ci.checkpoint_id where ci.user_id=? and ci.checkpoint_id=?)"
    user_stats = (
        col_roundsPlayed + col_roundsWon + col_pointsWon + col_tokensWon + col_isActive
    )
    keyname = " AND ci.user_id =?"

    conn, cursor = c.connect_db()

    try:
        logs = []
        query_statement = f"SELECT c.id, c.token_reward, c.point_reward, c.rounds, c.game_type, c.name{user_stats} FROM checkpoint c {inner_join}WHERE ci.checkpoint_id=?{keyname}"

        for i in range(0, len(checkId)):
            keyvalue = [
                user_id,
                checkId[i][0],
                user_id,
                checkId[i][0],
                user_id,
                checkId[i][0],
                user_id,
                checkId[i][0],
                user_id,
                checkId[i][0],
                checkId[i][0],
                user_id,
            ]
            cursor.execute(query_statement, keyvalue)
            log = cursor.fetchall()
            if log == []:
                response = Response(
                    "We couldn't grab the log", mimetype="plain/text", status=400
                )
                break

            card = {}
            response_key = [
                "checkpointId",
                "tokenReward",
                "pointReward",
                "rounds",
                "gameType",
                "gameName",
                "roundsPlayed",
                "roundsWon",
                "pointsWon",
                "tokensWon",
                "isActive",
            ]
            # if score is present
            for j in range(0, len(log[0])):
                if log[0][j] == None:
                    card[response_key[j]] = 0
                else:
                    card[response_key[j]] = log[0][j]
            logs.append(card)
    except KeyError:
        response = "Response"
        # need exceptions here

    c.disconnect_db(conn, cursor)

    if response != None:
        return response

    if logs != None:
        logs_json = json.dumps(logs, default=str)
        response = Response(logs_json, mimetype="application/json", status=200)

    if response == None:
        response = Response(
            "DbError: GET log - check_in catch", mimetype="plain/text", status=499
        )

    return response


# POST challenge results
def post(game_id, check_token, user_id, score):
    response = None

    conn, cursor = c.connect_db()

    try:
        # insert challenge result into table
        cursor.execute(
            "INSERT INTO check_in (game_id, checkpoint_id, user_id, is_winner) VALUE (?,(SELECT id FROM checkpoint WHERE check_token=?),?,?)",
            [game_id, check_token, user_id, score["isWin"]],
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

    return get(check_token, user_id, score)
