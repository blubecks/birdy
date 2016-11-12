from flask import Flask, jsonify, abort, request, render_template, send_from_directory
from BIRD.bird import Bird
import json


app = Flask(__name__)
app.config.from_pyfile('birdy.cfg')
bird = Bird(app)


@app.route("/api/session/all", methods=['GET'])
def get_all_session():
    return jsonify({"sessions": bird.all_bgp_session()})


@app.route("/api/session/<int:session_id>", methods=['GET'])
def get_single_session(session_id):
    abort(404)


@app.route("/api/configure/session", methods=['POST'])
def add_config():
    data = request.data
    data_dict = json.loads(data)
    return jsonify(bird.configure_new_session(data_dict))


@app.route("/", methods=['GET'])
def get_home():
    return render_template('index.html')


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
