import json
from tkinter import N
from flask import request, Response
import helpers.verification as verify
import challenges.r_p_s as rps
import dbinteractions.checkin as checkin
import dbinteractions.checkpoint as checkpoint


# GET check-in request to start challenge
def get():
    try:
        # input request
        user_id = request.args["userId"]
        check_token = request.args["checkToken"]
        # get checkpoint info
        data = checkpoint.get(check_token=check_token)
        if type(data) is not dict:
            return data
        score = checkin.get_score(user_id, check_token)
        if type(score) is not dict:
            return score
        response = data | score
        response_json = json.dumps(response, default=str)
        return Response(response_json, mimetype='application/json', status=200)
    except KeyError as ke:
        return Response(
            "KeyError: GET checkin - " + str(ke), mimetype="plain/text", status=500
        )
    except Exception as E:
        return Response("EndpointError: GET checkpoint - "+str(E), mimetype="plain/text", status=490)


# POST check-in request
def post():
    data = {}

    key = {
        0: "checkToken",
        1: "playerToken",
        2: "gameToken",
        3: "gameType",
        4: "playerChoice",
    }

    for i in range(0, len(key)):
        try:
            data[key[i]] = request.json[key[i]]
        except KeyError as ke:
            return Response(
                "KeyError: check-in POST " + str(ke), mimetype="plain/text", status=500
            )

    if data != {}:
        # verify login
        game_id, user_id = verify.player(data["playerToken"])
        # verify check
        if game_id == False:
            return user_id

    # prevent additional entries if game is not active
    # check to see if game is active
    if checkin.is_active(user_id, data["checkToken"]):
        challenge = {0: rps.game(data["playerChoice"])}
        # challenge results
        isWin, bot_choice, plyr_choice = challenge[data["gameType"]]
        score = {"isWin": isWin, "computer": bot_choice, "player": plyr_choice}
        # update database
        return checkin.post(game_id, data["checkToken"], user_id, score)
    
    # get checkpoint info if game is completed
    data = checkpoint.get(check_token=data["checkToken"])
    if type(data) is not dict:
        return data
    score = checkin.get_score(user_id, data["checkToken"])
    if type(score) is not dict:
        return score
    response = data | score
    response_json = json.dumps(response, default=str)
    return Response(response_json, mimetype='application/json', status=200)


# GET request for game logs
def get_log():
    try:
        # input request for user_id
        user_id = int(request.args["userId"])
        return checkin.get_log(user_id)
    except KeyError:
        return Response(
            "KeyError: 'user_id' keyname not present", mimetype="plain/text", status=500
        )
    except ValueError:
        return Response(
            "InputError: value entered for 'user_id' not valid",
            mimetype="plain/text",
            status=400,
        )
    except Exception as E:
        return Response("EndpointError: GET check-in log - catch "+str(E), mimetype="plain/text", status=499)

def get_standing():
    try:
        #input request for game_token
        game_token = request.args['gameToken']
        return checkin.get_standing(game_token)
    except KeyError as ke:
        return Response("KeyError: GET_LOG checkin "+str(ke), mimetype="plain/text", status=500)
    except Exception as E:
        return Response("EndpointError: GET_STANDING check-in - catch "+str(E), mimetype="plain/text", status=499)