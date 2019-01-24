from flask import Flask
from flask import request
import json

# Json with initial data
data = json.loads("""{
    "series": [
        {
            "name": "Narcos",
            "platform": "Netflix"
        },
        {
            "name": "The Punisher",
            "platform": "Netflix"
        },
        {
            "name": "Game of Thrones",
            "platform": "HBO"
        },
        {
            "name": "WestWorld",
            "platform": "HBO"
        }
    ],
    "films": [
        {
            "name":"Spectral",
            "platform": "Netflix"
        },
        {
            "name": "Men in Black",
            "platform": "HBO"
        }
    ]
}""")

# Creating instance of flask
app = Flask(__name__)


# Routes
@app.route("/")
def hello():
    if 'name' in request.args:
        return "Hello, {}".format(request.args['name'])
    else:
        return "Hello World"


@app.route("/series", methods=['GET', 'POST'])
def seriesOperation():
    # Get Method
    if request.method == "GET":
        values = json.dumps(data['series'])
        response = app.response_class(values, status=200, mimetype="application/json")

    #Post Method
    if request.method == "POST":
        #Get Data from request
        toInsert = request.data

        #Add the data from request to the array
        data['series'].append(json.loads(toInsert))

        response = app.response_class(json.dumps({"message":"ok"}), status=200, mimetype="application/json")


    return response

#Delete Series
@app.route("/series/<name>", methods=["DELETE"])
def deleteSerie(name):
    counter = 0
    deleted = False
    #Search serie
    for serie in data["series"]:
        if serie["name"] == name:
            print("Borro a ", serie)
            data["series"].pop(counter)
            deleted = True
        counter = +1
    if deleted:
        return  app.response_class(json.dumps({"message":"deleted"}), status=200, mimetype="application/json")
    else:
        return  app.response_class(json.dumps({"message":"error"}), status=500, mimetype="application/json")


@app.route("/films", methods=['GET', 'POST'])
def filmsOperation():
    # Get Method
    if request.method == "GET":
        values = json.dumps(data['films'])
        response = app.response_class(values, status=200, mimetype="application/json")

    #Post Method
    if request.method == "POST":
        #Get Data from request
        toInsert = request.data

        #Add the data from request to the array
        data['films'].append(json.loads(toInsert))

        response = app.response_class(json.dumps({"message":"ok"}), status=200, mimetype="application/json")


    return response


#Delete Series
@app.route("/films/<name>", methods=["DELETE"])
def deleteFilm(name):
    counter = 0
    deleted = False
    #Search serie
    for film in data["films"]:
        if film["name"] == name:
            print("Borro a ", film)
            data["films"].pop(counter)
            deleted = True
        counter = +1
    if deleted:
        return app.response_class(json.dumps({"message": "deleted"}), status=200, mimetype="application/json")
    else:
        return app.response_class(json.dumps({"message": "error"}), status=500, mimetype="application/json")

# Main Method
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)