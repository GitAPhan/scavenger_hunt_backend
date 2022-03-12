from flask import request, Response
import dbinteractions.user as db


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

