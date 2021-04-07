from flask import Flask, render_template, make_response, jsonify, request

app = Flask(__name__)


INFO = {
    "languages": {
        "es":"Spanish",
        "en":"English",
        "fr":"French"
    },
    "colors":{
        "r":"red",
        "g":"green",
        "b":"blue"
    },
    "clouds":{
        "IBM":"IBM CLOUD",
        "AMAZON":"AWS",
        "MICROSOFT":"AZURE"
    }
}

# GET METHOD

@app.route("/")
def home():
    return "<h1 style='color:blue'>This is home!!</h1>"

@app.route("/temp")
def template():
    return render_template('index.html')

@app.route("/qstr")
def query_string():
    if request.args:
        req=request.args
        res = {}
        for key, value in req.items():
            res[key] = value
        res = make_response(jsonify(res), 200)
        return res

    res = make_response(jsonify({"error":"No query string"}), 400)
    return res

@app.route("/json")
def get_json():
    res = make_response(jsonify(INFO), 200)
    return res


@app.route("/json/<collection>/<member>")
def get_data(collection, member):
    if collection in INFO:
        member = INFO[collection].get(member)
        if member:
            res = make_response(jsonify({"res":member}), 200)
            return res

        res = make_response(jsonify({"error":"Not found member"}), 400)
        return res

    res = make_response(jsonify({"error":"Not found collection"}), 400)
    return res


# POST METHOD

@app.route("/json/<collection>", methods=["POST"])
def create_colletion(collection):
    req = request.get_json()

    if collection in INFO:
        res = make_response(jsonify({"error":"Collection already exists"}))
        return res

    INFO.update({collection: req})

    res = make_response(jsonify({"message":"collection created"}), 201)
    return res


# PUT METHOD

@app.route("/json/<collection>/<member>", methods=["PUT"])
def update_colletion(collection, member):
    req = request.get_json()

    if collection in INFO:
        if member:
            INFO[collection][member] = req["new"]
            res = make_response(jsonify({"res":INFO[collection]}), 200)
            return res

        res = make_response(jsonify({"error":"Member not found"}), 200)
        return res


    res = make_response(jsonify({"error":"collection not found"}), 201)
    return res


# DELETE METHOD

@app.route("/json/<collection>", methods=["DELETE"])
def delete_collection(collection):
    req = request.get_json()

    if collection in INFO:
        del INFO[collection]
        res = make_response(jsonify(INFO), 400)
        return res


    res = make_response(jsonify({"error":"collection not found"}), 201)
    return res



if __name__ == "__main__":
    print("Server runnning")
    app.run(port = 3000, debug = True)