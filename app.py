from flask import Flask
import sys
import endpoints.user as user
import endpoints.login as login
import endpoints.game as game
import endpoints.checkin as checkin
import endpoints.checkpoint as checkpoint


app = Flask(__name__)


# # user requests
# GET user

# POST user
@app.post('/api/users')
def post_user():
    return user.post()


# # login requests
# used for username live check
@app.get('/api/login')
def get_username():
    return user.check()

# POST login attempt
@app.post('/api/login')
def post_login():
    return login.post()

# PATCH login - player login
@app.patch('/api/login')
def patch_login():
    return login.patch()

# # game requests
# 

# POST game
@app.post('/api/games')
def post_game():
    return game.post()

# # check-in requests
#GET check-in
@app.get('/api/check-in')
def get_check():
    return checkin.get()

# GET check-in log
@app.get('/api/check-in/log')
def get_check_log():
    return checkin.get_log()

@app.get('/api/check-in/standing')
def get_standing():
    return checkin.get_standing()

# POST check-in
@app.post('/api/check-in')
def post_check():
    return checkin.post()


# # checkpoint requests
# GET checkpoint info
@app.get('/api/checkpoints')
def get_checkpoint():
    return checkpoint.get()



# ## RUN MODE SETTINGS ##
# mode check
if len(sys.argv) > 1:
    mode = sys.argv[1]
else:
    print(
        "You must pass a mode to run this python script. Either 'testing' or 'production'"
    )
    exit()

# testing/production mode code
if mode == "testing":
    from flask_cors import CORS

    CORS(app)
    print("running in testing mode")
    app.run(debug=True)
elif mode == "production":
    print("running in production mode")
    import bjoern  # type: ignore

    bjoern.run(app, "0.0.0.0", 5005)
else:
    print("Invalid mode: Please run using either 'testing' or 'production'")
    exit()