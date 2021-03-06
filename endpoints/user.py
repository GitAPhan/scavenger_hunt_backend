import json
from flask import request, Response
import dbinteractions.checkin as checkin
import dbinteractions.user as user
import dbinteractions.login as login
import helpers.verification as verify


# GET user request
def get():
    response = None

    try:
        # input request user_id
        user_id = request.args['userId']
        # request to database
        response = user.get(user_id)
        if type(response) is not dict:
            return response
        return Response(json.dumps(response, default=str), mimetype="application/json", status=200)
    except KeyError:
        return Response("Endpoint Error: GET user - 'userId' keyname not present", mimetype="plain/text", status=500)
    except Exception as e:
        return Response("EndpointError: GET user - "+str(e), mimetype="plain/text", status=490)


# POST user request
def post():
    response = None

    # input request 
    keyvalue = {}

    # input keynames
    keyname = {
        1: 'username',
        2: 'email',
        3: 'isOver13',
        4: 'password',
        5: 'displayName',
        6: 'salt'
    }

    for i in range(1,6):
        try:
            keyvalue[keyname[i]] = request.json[keyname[i]]
        except KeyError as ke:
            print(ke)
            if i == 5:
                keyvalue[keyname[i]] = None
                pass
            else:
                return Response("KeyError: '"+keyname[i]+"' keyname not present", mimetype="plain/text", status=500)
        
        # more exceptions needed
    
    # hash password
    keyvalue['password'], keyvalue['salt'] = verify.create_password(keyvalue['password'])
    if isinstance(keyvalue['password'], str) and isinstance(keyvalue['salt'], str):
        response = user.post(keyvalue['username'], keyvalue['password'], keyvalue['salt'], keyvalue['email'], keyvalue['isOver13'], name=keyvalue['displayName'] )

    if response == None:
        response = Response("Endpoint Error: POST user - catch", mimetype="plain/text", status=499)
    
    return response

# live check username availability
def check():
    response = None

    try: 
        # input request for username
        username = request.args['username']
        if verify.username(username):
            response = user.check(username)
    except KeyError:
        return Response("KeyError: 'username' keyname not present", mimetype="plain/text", status=500)
    # need more exceptions

    if response == None:
        response = Response('username does not meet requirements', mimetype='plain/text', status=400)
    return response

# DEMO
# create demo account in database
# sign account into game
# create demo check-in to represent played, open and new games
def demo():
    response = None

    try:

        name = request.json['name']

        # create demo account
        status, demo_account = user.demo(name)
        if not status:
            raise Exception("user")

        # sign into demo game
        status, demo_game = login.demo(user_id=demo_account["userId"], name=name)
        if not status:
            raise Exception("game")

        # create demo check-in
        status = checkin.demo(demo_game["userId"])
        if not status:
            raise Exception("checkin")

    except KeyError:
        return Response("KeyError", mimetype="plain/text", status=490)
    except Exception as E:
        return Response("General Error - Demo "+str(E), mimetype='plain/text', status=490)

    response = {
        "gameToken": demo_game["gameToken"],
        "playerToken": demo_game["playerToken"],
        "gameName": demo_game["gameName"],
        "userId": demo_game["userId"],
        "username": demo_game["username"]
    }

    response_json = json.dumps(response, default=str)
    response = Response(response_json, mimetype="application/json", status=200)

    return response