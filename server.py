from flask import Flask, jsonify, abort, request, render_template, send_from_directory
from BIRD.bird import Bird
import json
import logging

logging.basicConfig(format='[%(asctime)s] %(message)s', filename='./logger.log', level=logging.INFO)

app = Flask(__name__)
app.config.from_pyfile('birdy.cfg')
bird = Bird(app)


@app.route("/api/session/all", methods=['GET'])
def get_all_session():
    status = Bird.get_daemons_status()
    return jsonify({"status": status,"sessions": bird.all_bgp_session()})


@app.route("/api/session/ipv4", methods=['GET'])
def get_ipv4_session():
    return jsonify({"sessions": bird.all_bgp_session('ipv4')})


@app.route("/api/session/ipv6", methods=['GET'])
def get_ipv6_session():
    return jsonify({"sessions": bird.all_bgp_session('ipv6')})


@app.route("/api/session/stats", methods=['GET'])
def get_all_session_stats():
    sessions_without_routes = bird.all_bgp_session()
    sessions = bird.enrich_session(sessions_without_routes)
    return jsonify({"sessions": sessions})


@app.route("/api/session/<int:session_id>", methods=['GET'])
def get_single_session(session_id):
    abort(404)


@app.route("/api/configure/session", methods=['POST'])
def add_config():
    try:
        data = request.data
    except ValueError as ve:
        return {
                'status': 'error',
                'message': ve.message
            }
    data_dict = json.loads(data)
    return jsonify(bird.configure_new_session(data_dict))


@app.route("/", methods=['GET'])
def get_home():
    return render_template('index.html')


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run(host=app.config['SERVER_HOST'])
