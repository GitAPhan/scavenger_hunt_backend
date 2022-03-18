import dbinteractions.dbinteractions as c
from flask import Response
import json
import mariadb as db

# GET challenge info
def get(user_id, game_id, check_token):
    response = None
    data = None

    conn, cursor = c.connect_db()

    try:
        # query to select game info(token_reward, point_reward, rounds, game_type) and game status(rounds_played, rounds_won, points_won, tokens_awarded)
        cursor.execute(
            "SELECT p.token_reward, p.point_reward, p.rounds, p.game_type, p.name, COUNT(c.id), (select count(c.id) from check_in c where c.is_winner=1), (select sum(p.point_reward) from check_in c inner join checkpoint p on p.game_id = c.game_id where c.user_id=? and c.is_winner=1), (select sum(p.token_reward) from check_in c inner join checkpoint p on p.game_id = c.game_id where c.user_id=? and c.is_winner=1) FROM checkpoint p INNER JOIN check_in c ON c.game_id = p.game_id WHERE p.check_token=? AND p.game_id=? and c.user_id =?",
            [user_id, user_id, check_token, game_id, user_id],
        )
        data = cursor.fetchall()[0]
        if not isinstance(data[0], int):
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

    if data != None:
        response = {
            "tokenReward": data[0],
            "pointReward": data[1],
            "rounds": data[2],
            "gameType": data[3],
            "gameName": data[4],
            "roundsPlayed": data[5],
            "roundsWon": data[6],
            "pointsWon": data[7],
            "tokensWon": data[8],
        }
        response_json = json.dumps(response, default=str)
        response = Response(response_json, mimetype="application/json", status=200)

    if response == None:
        response = Response(
            "DbError: GET check-in - catch", mimetype="plain/text", status=499
        )
    return response


# POST challenge results
def post(game_id, checkpoint_id, user_id, is_winner):
    response = None

    conn, cursor = c.connect_db()

    try:
        # insert challenge result into table
        cursor.execute(
            "INSERT INTO check_in (game_id, checkpoint_id, user_id, is_winner) VALUE (?,?,?,?)",
            [game_id, checkpoint_id, user_id, is_winner],
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
