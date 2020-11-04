from flask import request
import dataiku

from flask import session

app.secret_key = "something-from-os.urandom(24)"
app.session_cookie_name = "my-flask-session"

@app.before_request
def session_management():
    session.permanent = True
    
# set a value in the model
@app.route('/set', methods=['POST'])
def set():
    for k in ['X', 'Y']:
        if k in request.form:
            session[k] = request.form[k]
    return json.dumps({'X':session.get("X", None), 'Y':session.get("Y", None)})

# compute something based on the state of the model
@app.route('/get-plot', methods=['GET'])
def refresh_plot():
    x = session.get("X", 0)
    y = session.get("Y", 0)
    html = '<div style="background: blue; opacity: 0.5; position: absolute; left: %s%%; top: %s%%; width: 10px; height: 10px"></div>' % (x, y)
    return html
