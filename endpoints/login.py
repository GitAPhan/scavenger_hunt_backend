import re
from flask import request, Response
import dbinteractions.login as login
import helpers.verification as verify

# POST login session request
def post():
    response = None

    try:
        # input request for username
        username = request.json["username"]
        password = request.json["password"]
        # grab user credentials from database to verify
        hashpass, salt, user_id = verify.get_hashpass(username, "username")
        if hashpass == False:
            return salt
    except KeyError as KE:
        return Response(str(KE), mimetype="plain/text", status=500)

    # database request
    if verify.password(hashpass, salt, password):
        response = login.post(user_id, username)
    else:
        response = Response("login fail pass verify", mimetype="plain/text", status=403)

    # None check - catch
    if response == None:
        response = Response(
            "LoginError: POST - catch error", mimetype="plain/text", status=499
        )

    return response


# PATCH login session - used for players joining existing game
def patch():
    response = None
    Request = {}

    # input keynames
    keyname = {
        1: "tempToken",
        2: "loginId",
        3: "userId",
        4: "gameToken",
    }

    for i in range(1, len(keyname) + 1):
        try:
            Request[keyname[i]] = request.json[keyname[i]]
        except KeyError as ke:
            return Response(str(ke), mimetype="plain/text", status=500)

    if Request != {}:
        # verify tempToken
        status, username = verify.tempToken(
            Request["tempToken"], Request["loginId"], Request["userId"]
        )
        if status:
            # verify gameToken
            game_id, game_name = verify.gameToken(Request["gameToken"])
            if game_id == False:
                return game_name
            else:
                response = login.patch(
                    game_id,
                    username,
                    Request["userId"],
                    Request["tempToken"],
                    Request["loginId"],
                    game_name,
                    Request["gameToken"],
                )
        else:
            return username

    #         response = login.player(username, Request['userId'], Request['tempToken'], Request['loginId'], Request['gameToken'])
    #     else:
    #         return username

    if response == None:

        response = Response(
            "EndpointError: PATCH login - catch", mimetype="plain/text", status=499
        )

    return response
