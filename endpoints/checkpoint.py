import json
from flask import request, Response
import helpers.verification as verify
import challenges.r_p_s as rps
import dbinteractions.checkpoint as checkpoint

# GET checkpoint info request
def get():
    response = None
    data = {}

    # input request
    key = ['gameId', 'checkpointId', 'checkToken']
    try:
       for i in range(0, 2):
           data[key[i]] = request.args[key[i]]
    except KeyError as ke:
        if i == 0:
            return Response('KeyError: GET checkpoint -'+str(ke), mimetype="plain/text", status=500)
    # need more exceptions

    if data != {}:
        return checkpoint.get(game_id=data['gameId'])

    return Response('EndpointError: GET checkpoint - catch', mimetype="plain/text", status=490)