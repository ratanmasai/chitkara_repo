from flask import Flask, render_template, redirect, url_for


app = Flask(__name__)


@app.route("/")  # 127.0.0.1:5000/
def index():
    return render_template("index.html")


@app.route("/contact")  # 127.0.0.1:5000/contact
def contact():
    isValid = True

    if isValid:
        return redirect(url_for("profiles"))
        # return render_template("profile.html")
    else:
        return render_template("contact.html")


@app.route("/profile")  # 127.0.0.1:5000/profile
def profiles():

    return render_template("profile.html")


@app.route("/about")  # 127.0.0.1:5000/about
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
