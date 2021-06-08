#dependencies 
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

#set up Flask
app = Flask(__name__)


#set up connection 
conn = 'mongodb://localhost:27017'
mongo = PyMongo(app)

#routes

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

#scrape route/import mars.py script
@app.route("/scrape")
def scrapper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful"

# Define Main Behavior
if __name__ == "__main__":
    app.run()    

