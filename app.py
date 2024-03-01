# Citation for the following: app.py
# Date: 2/29/2024
# Copied from: Github 
# Source URL: https://github.com/DURepo/CS_325_Exercises/blob/main/Graph-calculate_distances.py

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

# Configuration

app = Flask(__name__)

# db_connection = db.connect_to_database()
# Routes 
@app.route("/")
def home():
    return redirect("/index")

app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_youngj9"
app.config["MYSQL_PASSWORD"] = "2754"
app.config["MYSQL_DB"] = "cs340_youngj9"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/index")
def index():
    return render_template("index.j2")

@app.route("/classes")
def classes():
    return render_template("classes.j2")

@app.route("/members")
def members():
    return render_template("members.j2")

@app.route("/memberships")
def memberships():
    return render_template("memberships.j2")

@app.route("/members_classes")
def members_classes():
    return render_template("members_classes.j2")


@app.route("/trainers", methods=["POST", "GET"])
def trainers():
    # Separate out the request methods, in this case this is for a POST
    # insert a person into the bsg_people entity
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Trainer"):
            # grab user form inputs
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]

            query = "INSERT INTO Trainers (firstName, lastName) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (firstName, lastName))
            mysql.connection.commit()

            # redirect back to people page
            return redirect("/trainers")

    # Grab bsg_people data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = "SELECT * FROM Trainers;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("trainers.j2", data=data)


# route for delete functionality, deleting a person from bsg_people,
# we want to pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/delete_trainers/<int:id>")
def delete_trainers(id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Trainers WHERE trainerID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/trainers")

# route for edit functionality, updating the attributes of a person in bsg_people
# similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/edit_trainers/<int:id>", methods=["POST", "GET"])
def edit_trainers(id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Trainers WHERE trainerID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_trainers.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("edit_trainers"):
            # grab user form inputs
            trainerID = request.form["trainerID"]
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]

            query = "UPDATE Trainers SET Trainers.firstName = %s, Trainers.lastName = %s WHERE Trainers.trainerID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (firstName, lastName, trainerID))
            mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect("/trainers")

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 61323)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True) 