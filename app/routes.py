import matplotlib
matplotlib.use('Agg')
from app import app
from app.form import TripSearchForm
from flask import render_template, flash, url_for
from app.gordian import GordianQuery
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = TripSearchForm()
    gord = GordianQuery(app.config["GORDIAN_API_KEY"])
    if form.validate_on_submit():
        results = None
        date_string = form.departure_date.data.strftime("%Y-%m-%d")
        trip_id = gord.createTrip()
        if trip_id == False:
            flash('Error: Failure to create trip')
        else:
            search_id = gord.startSearch(
                trip_id, form.departure_airport.data,
                form.arrival_airport.data,
                date_string,
                form.airline.data[-2:])
            if search_id == False:
                flash('Error: Failure to create search query')
            else:
                flash('Searching for trip from {} to {} leaving on {}'.format(
                    form.departure_airport.data, 
                    form.arrival_airport.data, 
                    form.departure_date.data))
                results = gord.getSearchResults(trip_id, search_id)
                if results == False:
                    flash('Error: Search for trip failed')
                img = io.BytesIO()
                fig, ax = plt.subplots()
                ax.hist(results["durations"], bins= 5)
                ax.set_ylabel('Number of tickets')
                ax.set_xlabel('Flight Duration (min)')
                plt.savefig(img, format='png')
                img.seek(0)
                plot_url = base64.b64encode(img.getvalue()).decode()
                return render_template('index.html', title='Search Trips', form=form, results=results, plot_url=plot_url)
    return render_template('index.html', title='Search Trips', form=form)
