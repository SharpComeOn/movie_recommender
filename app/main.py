import pandas as pd
from src.recommendater import Recommendater
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    user_id = '0'
    action = ""
    movie_title = ""
    if request.method == "POST":
        user_id = request.form["user_id"]
        movie_title = request.form["movie_title"].title().strip()
        action = request.form["action"]
        if (user_id.isnumeric() and int(user_id) > 0):
            message = "Welcome " + str(user_id)

    pd.set_option('colheader_justify', 'center')

    if (action == 'Content based'):
        if(movie_title != ""):
            df = genres_based(movie_title)
            if(isinstance(df, pd.DataFrame)):
                return render_template("index.html", welcome_message=message, tables=[df.to_html(classes='table_style', header="true")], titles=df.columns.values)
        else:
            return render_template("index.html", welcome_message="Please input a movie title to get recommendations of the same genres.")
    elif (action == 'Memory based' and user_id.isnumeric() and int(user_id) > 0):
        df = memory_based(user_id)
        if isinstance(df, pd.DataFrame):
            return render_template("index.html", welcome_message=message, tables=[df.to_html(classes='table_style', header="true")], titles=df.columns.values)
    else:
        return render_template("index.html")

def genres_based(movie_title):
    rec = Recommendater()
    return rec.genres_based(movie_title)

def memory_based(user_id):
    rec = Recommendater(user_id, "memory based")
    return rec.memory_based(user_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)