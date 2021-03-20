from flask import Flask, jsonify, render_template
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,inspect, desc
from sqlalchemy import Integer, Column, Float, String

engine = create_engine("postgres://pgadmin@pg-srv-001:ucN-xZRL3NsaBjvG2tcw1gPcsNeS5Xfw@pg-srv-001.postgres.database.azure.com:5432/netflix",connect_args={'sslmode':'require'})
conn = engine.connect()
Base = automap_base()
Base.prepare(engine, reflect=True)
#print (Base.classes.keys())

title = Base.classes.title
country = Base.classes.country
listed_in = Base.classes.listed_in
players = Base.classes.players
player_title = Base.classes.player_title
pg_rating = Base.classes.pg_rating
director = Base.classes.director
title = Base.classes.title
title_country = Base.classes.title_country
country = Base.classes.country
listed_in_title = Base.classes.listed_in_title
director_title = Base.classes.director_title

session = Session(engine)

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/index1")
def index1():
    return render_template("index1.html")

@app.route("/index2")
def index2():
    return render_template("index2.html")

####index3
@app.route("/index3")
def index3():
    return render_template("index3.html")

####index4
@app.route("/index4")
def index4():
    return render_template("index4.html")

####Index5 ROUTE
@app.route("/index5")
def index5():
    return render_template("index5.html")

####Index6 ROUTE
@app.route("/index6")
def index6():
    return render_template("index6.html")

####display All data
@app.route("/list_all_data")
def lista_all_data():
    return render_template("all_data.html")

@app.route("/api/v1.0/titles")
def titles():
    allTitles = []
    Titles = session.query(title.title,title.description,title.date_added).all()
    for result in Titles:
        row = {}
        row["title"] = result[0]
        row["description"] = result[1]
        row["date_added"] = result[2]
        allTitles.append(row)
    return jsonify(allTitles)

@app.route("/api/v1.0/countries")
def countries():
    allCountries = []
    Countries = session.query(country.country_id, country.country_name, country.longitude, country.latitude).all()
    for result in Countries:
        row = {}
        row["country_id"] = result[0]
        row["country_name"] = result[1]
        row["longitude"] = result[2]
        row["latitude"] = result[3]
        allCountries.append(row)
    return jsonify(allCountries)

####Country vs y: Count of Titles, drop down: Year ----done
@app.route("/api/v1.0/titles_country")
def titles_country():
    titles_countries_years= []
    countries_count = session.query (country.country_name, title.release_year, func.count(title.show_id)).filter(title.show_id==title_country.show_id,).filter(title_country.country_id == country.country_id).group_by(country.country_name, title.release_year).all()
    for result in countries_count:
        row = {}
        row["country_name"] = result[0]
        row["release_year"] = result[1]
        row["Count_of_Titles"] = result[2]
        titles_countries_years.append(row)
    return jsonify(titles_countries_years)

####x: Budget vs y: Movie Revenue 
@app.route("/api/v1.0/budget_revenue")
def budget_revenue():
    budget_revenue_all= []
    budget_revenue = session.query (title.budget, title.revenue).filter(title.budget!=0,).filter(title.revenue != 0).all()
    for result in budget_revenue:
        row = {}
        row["Budget"] = result[0]
        row["Revenue"] = result[1]
        budget_revenue_all.append(row)
    return jsonify(budget_revenue_all)

####x: Budget vs y: rating
@app.route("/api/v1.0/pgrating_totalbudget")
def pgrating_totalbudget():
    pgrating_totalbudget_all= []
    pgrating_totalbudget = session.query (pg_rating.pg_rating_name, func.sum(title.budget)).filter(title.pg_rating_id==pg_rating.pg_rating_id).group_by(pg_rating.pg_rating_name).all()
    for result in pgrating_totalbudget:
        row = {}
        row["PG_Rating"] = result[0]
        row["Total_budget"] = result[1]
        pgrating_totalbudget_all.append(row)
    return jsonify(pgrating_totalbudget_all)

####x: Budget vs y: Country
@app.route("/api/v1.0/country_budget")
def country_budget():
    country_budget_all= []
    country_budget = session.query (country.country_name, func.sum(title.budget)).filter(title.show_id == title_country.show_id,).filter(title_country.country_id == country.country_id).group_by(country.country_name).all()
    for result in country_budget:
        row = {}
        row["country_name"] = result[0]
        row["budget"] = result[1]
        country_budget_all.append(row)
        print (jsonify(country_budget_all)) 
    return jsonify(country_budget_all)

####Budget all graphs
@app.route("/api/v1.0/country_year_budget_revenue")
def country_year_budget_revenue():
    country_year_budget_revenue = []
    country_year_budget_revenue_all= []

    country_year_budget_revenue = session.query (country.country_name, title.release_year, func.sum(title.budget), func.sum(title.revenue), func.count(title.show_id))\
        .filter(country.country_id == title_country.country_id,)\
        .filter(title_country.show_id == title.show_id)\
        .group_by(country.country_name, title.release_year)\
        .order_by(desc(title.release_year))\
        .all()
    
    for result in country_year_budget_revenue:
        row = {}
        row["Country"] = result[0]
        row["ReleaseYear"] = result[1]
        row["TotalBudget"] = result[2]
        row["TotalRevenue"] = result[3]
        row["TitleCount"] = result[4]

        country_year_budget_revenue_all.append(row)
    
    return jsonify(country_year_budget_revenue_all)

####x: Listed In vs y: Count of titles
@app.route("/api/v1.0/listedin_count")
def listedin_count():
    listedin_count_all= []
    listedin_count = session.query (listed_in.listed_in_name, func.count(title.show_id)).filter(title.show_id == listed_in_title.show_id,).filter(listed_in.listed_in_id == listed_in_title.listed_in_id).group_by(listed_in.listed_in_name).limit(10).all()
    for result in listedin_count:
        row = {}
        row["Listed_in_name"] = result[0]
        row["Count"] = result[1]
        listedin_count_all.append(row)
    return jsonify(listedin_count_all)

####x: Directors vs Count per release year
@app.route("/api/v1.0/directors_titlecount")
def directors_titlecount():
    directors_titlecount_all= []
    directors_titlecount = session.query (director.director_name, title.release_year, func.count(title.show_id)).filter(director.director_id == director_title.director_id,).filter(title.show_id == director_title.show_id).group_by(director.director_name, title.release_year).all()
    for result in directors_titlecount:
        row = {}
        row["DirectorsName"] = result[0]
        row["ReleaseYear"] = result[1]
        row["TitleCount"] = result[2]
        directors_titlecount_all.append(row)
    return jsonify(directors_titlecount_all)

####x: Directors vs Revenue per release year
@app.route("/api/v1.0/directors_revenue")
def directors_revenue():
    directors_revenue_all= []
    directors_revenue = session.query (director.director_name, title.release_year, func.sum(title.revenue)).filter(director.director_id == director_title.director_id,).filter(title.show_id == director_title.show_id).group_by(director.director_name, title.release_year).all()
    for result in directors_revenue:
        row = {}
        row["director_name"] = result[0]
        row["release_year"] = result[1]
        row["revenue"] = result[2]
        directors_revenue_all.append(row)
    return jsonify(directors_revenue_all)

####x: Directors vs Revenue per release year
@app.route("/api/v1.0/directors_count_revenue")
def directors_count_revenue():
    directors_count_revenue = []
    directors_titlecount_all= []
    directors_revenue_all= []
    directors_revenue = session.query (director.director_name, title.release_year, func.sum(title.revenue), func.count(title.show_id))\
        .filter(director.director_id == director_title.director_id,)\
        .filter(title.show_id == director_title.show_id)\
        .group_by(title.release_year, director.director_name)\
        .order_by(desc(func.count(title.show_id)))\
        .all()
    for result in directors_revenue:
        row = {}
        row["Director_Name"] = result[0]
        row["ReleaseYear"] = result[1]
        row["Revenue"] = result[2]
        row["TitleCount"] = result[3]        
        directors_revenue_all.append(row)
    directors_count_revenue.append(directors_revenue_all)
    return jsonify (directors_revenue_all)

@app.route("/api/v1.0/players_count_revenue")
def players_count_revenue():
    players_count_revenue = []
    players_revenue_all= []
    players_revenue = session.query (players.player_name, title.release_year, func.sum(title.revenue), func.count(title.show_id))\
        .filter(players.player_id == player_title.player_id,)\
        .filter(title.show_id == player_title.show_id)\
        .group_by(title.release_year, players.player_name)\
        .order_by(desc(func.count(title.show_id)))\
        .all()
    for result in players_revenue:
        row = {}
        row["player_Name"] = result[0]
        row["ReleaseYear"] = result[1]
        row["Revenue"] = result[2]
        row["TitleCount"] = result[3]        
        players_revenue_all.append(row)
    players_count_revenue.append(players_revenue_all)
    return jsonify (players_revenue_all)
    
####x: year vs y: revenue for each player
@app.route("/api/v1.0/release_year_revenue")
def release_year_revenue():
    release_year_revenue_all= []
    release_year_revenue = session.query (title.release_year, players.player_name, func.sum(title.revenue)).filter(player_title.show_id == title.show_id,).filter(players.player_id == player_title.player_id).group_by(players.player_name,title.release_year).order_by(desc(func.sum(title.revenue))).all()
    for result in release_year_revenue:
        row = {}
        row["release_year"] = result[0]
        row["player_name"] = result[1]
        row["revenue"] = result[2]
        release_year_revenue_all.append(row)
    return jsonify(release_year_revenue_all)

####Export all data
@app.route("/api/v1.0/all_data")
def all_data():
    all_data= []
    all_data_query = session.query (title.show_id, title.title, title.date_added, title.release_year, title.duration, title.description, pg_rating.pg_rating_name, title.imdb_rating, title.rotten_tomatoes_rating, title.award, title.released_date, title.budget, title.revenue, country.country_name, director.director_name, listed_in.listed_in_name, players.player_name)\
            .filter(title.pg_rating_id == pg_rating.pg_rating_id,)\
            .filter(title_country.show_id == title.show_id,)\
            .filter(country.country_id == title_country.country_id,)\
            .filter(title.show_id == director_title.show_id,)\
            .filter(director_title.director_id == director.director_id,)\
            .filter(title.show_id == listed_in_title.show_id,)\
            .filter(listed_in.listed_in_id == listed_in_title.listed_in_id,)\
            .filter(title.show_id == player_title.show_id,)\
            .filter(player_title.player_id == players.player_id)\
            .order_by(desc(title.show_id)).limit(200).all()
    for result in all_data_query:
        row = {}
        row["show_id"] = result[0]
        row["title"] = result[1]
        row["date_added"] = result[2]
        row["release_year"] = result[3]
        row["duration"] = result[4]
        row["description"] = result[5]
        row["pg_rating"] = result[6]
        row["imdb_rating"] = result[7]
        row["rotten_tomatoes_rating"] = result[8]
        row["awards"] = result[9]
        row["released_date"] = result[10]
        row["budget"] = result[11]
        row["revenue"] = result[12]
        row["country_name"] = result[12]
        row["director_name"] = result[14]
        row["listed_in"] = result[15]
        row["player_name"] = result[16]
        all_data.append(row)
    return jsonify(all_data)

# 4. Define main behavior

if __name__ == "__main__":
    app.run(debug=True)