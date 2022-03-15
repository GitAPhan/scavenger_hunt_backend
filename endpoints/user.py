import json
from flask import Flask, request, Response
import dbinteractions.user as user
import helpers.verification as verify


# GET user request
def get():
    response = None

    try:
        # input request user_id
        user_id = request.args['userId']
        # request to database
        response = db.get(user_id)
    except KeyError:
        return Response("Endpoint Error: GET user - 'userId' keyname not present", mimetype="plain/text", status=500)

    if response == None:
        response = Response("Endpoint Error: GET user - catch", mimetype="plain/text", status=499)

    return response    


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
                i = 4
                pass
            else:
                return Response("KeyError: '"+keyname[i]+"' keyname not present", mimetype="plain/text", status=500)
        
        # more exceptions needed
    
    # hash password
    keyvalue[keyname[4]], keyvalue[keyname[6]] = verify.create_password(keyvalue['password'])

    if i == 4:
        response = user.post(keyvalue[keyname[1]], keyvalue[keyname[4]], keyvalue[keyname[6]], keyvalue[keyname[2]], keyvalue[keyname[3]] )
    else:
        response = user.post(keyvalue[keyname[1]], keyvalue[keyname[4]], keyvalue[keyname[6]], keyvalue[keyname[2]], keyvalue[keyname[3]], name=keyvalue[keyname[5]] )


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
