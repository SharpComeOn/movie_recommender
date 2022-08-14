# from src.calculator import Calculator
from flask import Flask, render_template, request

# cal = Calculator()
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    user_id = 0
    action = ""
    if request.method == "POST":
        user_id = request.form["user_id"]
        action = request.form["action"]

        result = "Welcome" + str(user_id) + action

    return render_template("index.html", result=result)

@app.route("/health")
def health():
    return "I am healthy"

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)