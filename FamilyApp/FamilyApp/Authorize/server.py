from flask import Flask, jsonify, request
app = Flask("__main__")

# sample get request
@app.route("/", methods=['GET'])
def responseHandler():
    r = request.args.get('code', '')
    file = open("Textfiles\\authCode.txt",'w')
    file.write(r)
    file.close()
    shutdown_server()
    #q.put(r)
    return r
    
    
    #return jsonify({"content": "Hello World!"})

# sample post request
@app.route("/", methods=['POST'])
def incr():
    return jsonify({"content": int(request.values["num"])+1})

#@app.route('/shutdown', methods=['GET'])
#def seriouslykill():
#    func = request.environ.get('werkzeug.server.shutdown')
#    if func is None:
#        raise RuntimeError('Not running with the Werkzeug Server')
#    func()
#    return "Shutting down..."

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def flaskThread():
    app.run(host='0.0.0.0', port=4321, use_reloader=False)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4321, use_reloader=False) # change the port to your liking
