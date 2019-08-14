# https://docs.cs50.net/2019/x/psets/7/survey/survey.html
# Implement a web app that enables a user to
# fill out a form, a la Google Forms, the results of which are saved to a comma-separated-value (CSV) file on the server, and
# view a table of all of the submissions received, a la Google Sheets.

import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request, url_for

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect(url_for("get_form"))


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    # Initialize an error counter
    errors = 0
    errorMessage = "There was errors in your submission, please review the following points then try to submit again:<br /><ul>"

    name = ""
    house = ""
    position = ""

    # Check for valid name input
    if not request.form.get("name") or len(request.form.get("name")) < 2:
        errors = errors + 1
        errorMessage = errorMessage + "<li>You need to enter a valid name</li>"
    else:
        # If a valid name was provided, save it
        name = request.form.get("name")

    # Check for valid house input
    if not request.form.get("house") or len(request.form.get("house")) < 6:
        errors = errors + 1
        errorMessage = errorMessage + "<li>You need to choose a house</li>"
    else:
        house = request.form.get("house")

    # Check for valid position input
    if not request.form.get("position") or len(request.form.get("position")) < 6:
        errors = errors + 1
        errorMessage = errorMessage + "<li>You need to choose a position</li>"
    else:
        position = request.form.get("position")

    # If the user input contains errors, redirect the user to the form with an error message
    if errors > 0:
        errorMessage = errorMessage + "</ul>"
        return render_template("form.html", errorMessage=errorMessage, name=name)

    # If the user input is valid, save the submission to our CSV file
    with open('survey.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([name, house, position])

    # Then redirect the user to the sheet page so he can view his submission
    return redirect(url_for("get_sheet"))


@app.route("/sheet", methods=["GET"])
def get_sheet():
    rows = []

    # Open our CSV file to parse it
    with open('survey.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        # Sending our data to our template
        return render_template("sheet.html", rows=reader)