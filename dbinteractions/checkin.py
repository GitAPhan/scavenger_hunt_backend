from asyncio.windows_events import NULL
import dbinteractions.dbinteractions as c
from flask import Response
import json
import mariadb as db

# GET challenge info
def get(check_token, user_id=None, score=None):
    response = None
    data = None

    # let the crazy query building begin!!
    inner_join = "INNER JOIN check_in c ON c.game_id = p.game_id "
    col_roundsPlayed = ", COUNT(c.id), "
    col_roundsWon ="(select count(c.id) from check_in c where c.is_winner=1), "
    col_pointsWon = "(select sum(p.point_reward) from check_in c inner join checkpoint p on p.game_id = c.game_id where c.user_id=? and c.is_winner=1), "
    col_tokensWon = "(select sum(p.token_reward) from check_in c inner join checkpoint p on p.game_id = c.game_id where c.user_id=? and c.is_winner=1)"
    col_isActive = ", (select if(p.rounds=count(c.id),'false','true'))"
    user_stats= col_roundsPlayed+col_roundsWon+col_pointsWon+col_tokensWon+col_isActive
    keyname = " AND c.user_id =?"
    keyvalue = [user_id, user_id, check_token, user_id]
    if user_id == None:
        inner_join = ""
        user_stats = ""
        keyname = ""
        keyvalue = [check_token]
    query_statement = f"SELECT p.token_reward, p.point_reward, p.rounds, p.game_type, p.name{user_stats} FROM checkpoint p {inner_join}WHERE p.check_token=?{keyname}"
    
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
        "tokenReward",
        "pointReward",
        "rounds",
        "gameType",
        "gameName",
        "roundsPlayed",
        "roundsWon",
        "pointsWon",
        "tokensWon",
        "isActive"
    ]

    if data != None:
        response = {}
        # if score is present
        if score != None:
            response['lastRound'] = score
        for i in range(0, len(data[0])):
            if (data[0][i] == None):
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


# POST challenge results
def post(game_id, check_token, user_id, score):
    response = None

    conn, cursor = c.connect_db()

    try:
        # insert challenge result into table
        cursor.execute(
            "INSERT INTO check_in (game_id, checkpoint_id, user_id, is_winner) VALUE (?,(SELECT id FROM checkpoint WHERE check_token=?),?,?)",
            [game_id, check_token, user_id, score['isWin']],
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