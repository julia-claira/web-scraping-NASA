from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape

app = Flask(__name__)

#set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/phone_app"
mongo = PyMongo(app)

#runs scrape function and updates db with the dictionary
@app.route("/scrape")
def scraper():
    facts = mongo.db.facts
    facts_data = scrape()
    facts.update({}, facts_data, upsert=True)
    return redirect("/", code=302)
    

#queries mongo db and passes results into html   
@app.route("/")
def index():
    facts = mongo.db.facts.find_one()
    return render_template("index.html", facts=facts)

if __name__ == "__main__":
    app.run(debug=True)
