from flask import Flask
from flask import request
import json
from flask import jsonify

from FlaskWithORM.encoder import Encoder
from FlaskWithORM.models.models import User
from database import db_session, init_db

# Creating instance of flask
app = Flask(__name__)
app.json_encoder = Encoder

# Close connection on-demand
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# Routes
@app.route("/users", methods=['GET', 'POST'])
def getUsers():
    if request.method == 'GET':
        data = User.query.all()
        print(data)
        return jsonify(data)
    elif request.method == 'POST':
        request_data = json.loads(request.data)
        print(request_data)
        u = User(request_data['name'], request_data['email'])
        db_session.add(u)
        db_session.commit()
        return app.response_class(json.dumps({"message": "ok"}), status=200, mimetype="application/json")

@app.route("/users/<string:emailUser>", methods=['GET', 'DELETE'])
def getDeleteUser(emailUser):
    if request.method == 'GET':
        data = User.query.filter_by(email= emailUser).first()
        if data is not None:
            return jsonify(data)
        else:
            return app.response_class(json.dumps({"message": "not found"}), status=404, mimetype="application/json")

    if request.method == 'DELETE':
        try:
            db_session.delete(User.query.filter_by(email= emailUser).first())
            db_session.commit()
            return  app.response_class(json.dumps({"message":"deleted"}), status=200, mimetype="application/json")
        except Exception:
            return  app.response_class(json.dumps({"message":"error"}), status=500, mimetype="application/json")


if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=3000)
