from flask import request, Response
import dbinteractions.game as game
import dbinteractions.login as login
import helpers.verification as verify


# 


# POST game
def post():
    response = None
    Request = {}

    # input keynames
    keyname = {
        1: 'loginToken',
        2: 'loginId',
        3: 'userId',
        4: 'gameName',
    }

    for i in range(1,5):
        try:
            Request[keyname[i]] = request.json[keyname[i]]
        except KeyError as ke:
            return Response(str(ke), mimetype="plain/text", status=500)
    
    if Request != {}:
        # verify loginToken
        status, username = verify.loginToken(Request['loginToken'], Request['loginId'], Request['userId'])
        if status:
            game_token, game_id = game.post(Request['gameName'], Request['userId'])
            # status_check
            if game_token == False:
                return game_id
            # login user to game
            response = login.patch(game_id, username, Request['userId'], Request['loginToken'], Request['loginId'], Request['gameName'], game_token, True)
    
    if response == None:
        response = Response("EndpointError: POST game - catch", mimetype='plain/text', status=499)
    
    return response