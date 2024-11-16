from flask import make_response, jsonify

def json_response(data, status_code=200):
    response = make_response(jsonify(data), status_code)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    return response