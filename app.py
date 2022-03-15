from flask import Flask
import sys
import endpoints.user as user


app = Flask(__name__)

# # user requests
# GET user

# POST user
@app.post('/api/users')
def post_user():
    return user.post()

# used for username live check
@app.get('/api/login')
def get_username():
    return user.check()






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