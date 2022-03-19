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
        1: "userId",
    }

    for i in range(0, len(key)):
        try:
            data[key[i]] = request.args[key[i]]
        except KeyError as ke:
            if i == 1:
                data[key[i]] = None
            else:
                return Response(str(ke), mimetype="plain/text", status=500)

    if data != {}:
        response = checkin.get(data['checkToken'],data['userId'])
    
    if response == None:
        response = Response('EndpointError: GET check-in - catch', mimetype='plain/text', status=499)
    return response    


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
            return Response('KeyError: check-in POST '+str(ke), mimetype="plain/text", status=500)
    
    if data != {}:
        # verify login
        game_id, user_id = verify.player(data['playerToken'])
        # verify check
        if game_id == False:
            return user_id
    
    challenge = {
        0: rps.game(data['playerChoice'])
    }
    # challenge results
    isWin, bot_choice, plyr_choice = challenge[data['gameType']]
    score = {
            "isWin": isWin,
            'computer': bot_choice,
            'player': plyr_choice
        }
    # update database
    return checkin.post(game_id, data['checkToken'], user_id, score)
    