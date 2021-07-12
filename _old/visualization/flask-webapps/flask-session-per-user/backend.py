from flask import request
import dataiku
import random

# global variable to store the models for all users of the webapp
model_per_view = {}
# accessor for the model of a given user
def get_model_for_view():
    global model_per_view
    # fetch the view identifier
    request_headers = dict(request.headers)
    identifier = request_headers.get('Flask-View-Id', None)
    if identifier is None:
        raise Exception("View identifier not set")
    # use the model for that particular identifier
    if identifier not in model_per_view:
        model_per_view[identifier] = {}
    return model_per_view[identifier]

# set a value in the model
@app.route('/set', methods=['POST'])
def set():
    model = get_model_for_view()
    for k in ['X', 'Y']:
        if k in request.form:
            model[k] = request.form[k]
    return json.dumps(model)

# compute something based on the state of the model
@app.route('/get-plot', methods=['GET'])
def refresh_plot():
    model = get_model_for_view()
    x = model.get("X", 0)
    y = model.get("Y", 0)
    html = '<div style="background: blue; opacity: 0.5; position: absolute; left: %s%%; top: %s%%; width: 10px; height: 10px"></div>' % (x, y)
    return html
