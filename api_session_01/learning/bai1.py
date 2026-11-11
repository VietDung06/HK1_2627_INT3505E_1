from flask import Flask

app = Flask(__name__)

@app.route('/welcome')
def welcome_user() :
    return {"status": "success", "content": "Hi, welcome to my API!"}

if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 8080, debug = True)