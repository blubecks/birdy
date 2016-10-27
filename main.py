from flask import Flask, jsonify, abort
from BIRD import bird
app = Flask(__name__)

sessions = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route("/api/session/all", methods=['GET'])
def get_all_session():
    return jsonify({"sessions":bird.greetings("andrea")})

@app.route("/api/session/<int:session_id>", methods=['GET'])
def get_single_session(session_id):
    session = [session for session in sessions if session['id']==session_id]
    if len(session)>0:
        return jsonify({'session':session})
    else:
        abort(404)



if __name__ == "__main__":
    app.run()
