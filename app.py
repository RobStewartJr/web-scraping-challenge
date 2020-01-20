from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():
    mars_information = mongo.db.mars.find_one()

    return render_template("index.html", mars_information = mars_information)

@app.route("/scrape")
def scrape():
    mars_information = mongo.db.mars_information
    mars_data = scrape_mars.scrape_news()
    mars_data = scrape_mars.scrape_image()
    mars_data = scrape_mars.scrape_facts()
    mars_data = scrape_mars.scrape_weather()
    mars_data = scrape_mars.scrape_hemispheres()
    mars_information.update({}, mars_data, upsert=True)

    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)