import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "quotesdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)
class Entry(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    quote = db.Column(db.String(1000))
    source = db.Column(db.String(100))
    note = db.Column(db.String(1000), nullable=True)


@app.route("/")
def index():
	result = Entry.query.all()

	return render_template("index.html", result=result)

@app.route("/sign")
def sign():
	return render_template("sign.html")

@app.route("/process", methods=["POST"])
def process():
    quote = request.form["quote"]
    source = request.form["source"]
    note = request.form["note"]
    
    signature = Entry(quote=quote, source=source, note=note)
    db.session.add(signature)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/delete", methods=["POST"])
def delete():
    quote = request.form.get("quote")

    quote = Entry.query.filter_by(quote=quote).first()
    db.session.delete(quote)

    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
	app.run(debug=True)
