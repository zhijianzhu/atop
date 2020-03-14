from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    #app.run_server(host="0.0.0.0",debug=True, port=5000)
    app.run(host='0.0.0.0')
