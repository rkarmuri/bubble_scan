from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/test', methods = ['GET'])

def test():
    
    return jsonify({"message": "Server is working!"})

if __name__ == '__main__':
    
    app.run(debug = True, port = 5000)