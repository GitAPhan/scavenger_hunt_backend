import json
from flask import request, Response
import helpers.verification as verify
import challenges.r_p_s as rps
import dbinteractions.checkin as checkin


# GET check-in request to start challenge
def get():
    response = None
    data = {}

    key = {
        0: "checkToken",
        1: "playerToken",
        2: "gameToken"
    }

    for i in range(0, len(key)):
        try:
            data[key[i]] = request.json[key[i]]
        except KeyError as ke:
            return Response(str(ke), mimetype="plain/text", status=500)

    if data != {}:
        #verify login
        game_id, user_id = verify.player(data['playerToken'])
        # status check
        if game_id == False:
            return user_id
        response = checkin.get(user_id, game_id, data['checkToken'])
    
    if response == None:
        response = Response('EndpointError: GET check-in - catch', mimetype='plain/text', status=499)
    return response    


# POST check-in request
def post():
    response = None
    r_data = {}

    key = {
        0: "checkToken",
        1: "playerToken",
        2: "gameToken",
        3: "gameType",
        4: "playerChoice",
    }
    
    for i in range(0, len(key)):
        try:
            r_data[key[i]] = request.json[key[i]]
        except KeyError as ke:
            return Response(str(ke), mimetype="plain/text", status=500)
    
    if r_data != {}:
        # verify login
        game_id, user_id = verify.player(r_data['playerToken'])
        # verify check
        if game_id == False:
            return user_id
    
    challenge = {
        0: rps.game(r_data['playerChoice'])
    }
    # challenge results
    score, bot_choice, plyr_choice = challenge[r_data['gameType']]

    # update database


    response = {
        "score": score,
        'bot_choice': bot_choice,
        'plyr_choice': plyr_choice
    }
    response_json = json.dumps(response, default=str)
    return Response(response_json, mimetype="plain/text", status=200)