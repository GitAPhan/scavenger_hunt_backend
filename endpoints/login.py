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
        1: "loginToken",
        2: "loginId",
        3: "userId",
        4: "gameToken",
    }
    
    for i in range(1, len(keyname) + 1):
        try:
            Request[keyname[i]] = request.json[keyname[i]]
        except KeyError as ke:
            return Response("KeyError"+str(ke), mimetype="plain/text", status=500)

    if Request != {}:
        # verify loginToken
        status, username = verify.loginToken(
            Request["loginToken"], Request["loginId"], Request["userId"]
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
                    Request["loginToken"],
                    Request["loginId"],
                    game_name,
                    Request["gameToken"],
                )
        else:
            return username

    if response == None:

        response = Response(
            "EndpointError: PATCH login - catch", mimetype="plain/text", status=499
        )

    return response


# logout DELETE login session
def delete():
    try:
        # input request for login_token
        login_token = request.json['loginToken']
        return login.delete(login_token=login_token)
    except KeyError:
        pass

    try:
        # input request for player_token
        player_token = request.json['playerToken']
        return login.delete(player_token=player_token)
    except KeyError:
        pass

    try:
        # input request for master_token
        master_token = request.json['masterToken']
        return login.delete(master_token=master_token)
    except KeyError:
        pass

    return Response("EndpointError: DELETE login - nothing happened", mimetype="plain/text", status=490)