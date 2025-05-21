
from flask import Flask, render_template, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)

DB_PATH = "database/relational_database.db"

def get_db_connection():
    conn = sqlite3.connect("database/relational_database.db")
    conn.row_factory = sqlite3.Row
    return conn

#CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET"]) 
@app.route("/")
def home():
    return render_template("home.html")



@app.route("/patterns")
def patterns():
    return render_template("patterns.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/visualization", methods = ["GET"])
def visualization():
    countries = get_countries()
    items = get_items()
    return render_template("visualization.html", countries = countries, country_items=items)
def get_countries():
    connection_db = sqlite3.connect(DB_PATH)
    query = "SELECT DISTINCT name FROM country"
    countries = pd.read_sql(query, connection_db)
    connection_db.close()
    return countries.to_dict(orient = "records")
def get_items():
    connection_db = sqlite3.connect(DB_PATH)
    connection_db.row_factory = sqlite3.Row
    cursor = connection_db.cursor()
    cursor.execute("SELECT * FROM item_table")
    items = cursor.fetchall()
    connection_db.close()
    return [dict(item) for item in items] 




@app.route("/api/country/<name>")
def get_country_data(name):
    conn = get_db_connection()
    scores = conn.execute(
        "SELECT Year, Score FROM score_table WHERE Country = ? ORDER BY Year",
        (name,)
    ).fetchall()
    incidents = conn.execute(
        'SELECT "Date of incident", "Incident name", "Brief description of the incident" FROM item_table WHERE "Country where incident took place" = ? ORDER BY "Year of incident"',
        (name,)
    ).fetchall()
    conn.close()

    

    return jsonify({
    'scores': [dict(row) for row in scores],
    'incidents': [dict(row) for row in incidents]
})

if __name__ == "__main__":
    app.run(debug=True)






