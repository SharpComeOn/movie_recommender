from src.recommendater import Recommendater
from flask import Flask, render_template, request

# cal = Calculator()
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    user_id = 0
    action = ""
    if request.method == "POST":
        user_id = request.form["user_id"]
        action = request.form["action"]

        message = "Welcome " + str(user_id) + ", you clicked button of " + action

    return render_template("index.html", welcome_message=message, tables=[method1().to_html(classes='data', header="true")], titles=method1().columns.values)

@app.route("/health")
def method1():
    rec = Recommendater("123", "Collaborative filtering")
    return rec.method1()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)