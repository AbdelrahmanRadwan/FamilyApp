from flask import Flask, jsonify, request
app = Flask("__main__")


# sample get request
@app.route("/", methods=['GET'])
def responseHandler():
    r = request.args.get('code', '')
    print(r)
    return
    #return jsonify({"content": "Hello World!"})

# sample post request
@app.route("/", methods=['POST'])
def incr():
    return jsonify({"content": int(request.values["num"])+1})

def flaskThread():
    app.run(host='0.0.0.0', port=4321, use_reloader=False)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4321) # change the port to your liking
