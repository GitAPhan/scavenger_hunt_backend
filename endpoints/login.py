from flask import request, Response
import dbinteractions.login as login
import helpers.verification as verify

# POST login session request
def post():
    response = None

    try:
        # input request for username
        username = request.json['username']
        password = request.json['password']
        # grab user credentials from database to verify
        hashpass, salt, user_id = verify.get_hashpass(username, "username")
        if hashpass == False:
            return salt
    except KeyError as KE:
        return Response(str(KE), mimetype='plain/text', status=500)
        
    # database request
    if verify.password(hashpass, salt, password):
        response = login.post(user_id, username)
    else:
        response = Response("login fail pass verify", mimetype="plain/text", status=403)
    
    # None check - catch
    if response == None:
        response = Response("LoginError: POST - catch error", mimetype='plain/text', status=499)
    
    return response