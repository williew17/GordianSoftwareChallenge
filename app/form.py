from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField, DateField
from wtforms.validators import DataRequired, Regexp

AIRLINES = ['Lufthansa - LH', 'Southwest - WN']

class TripSearchForm(FlaskForm):
    departure_airport = StringField(label='Departure Airport', 
                                    validators=[DataRequired(), 
                                                Regexp('^[A-Z]{3}$', message="Must use IATA code format")])
    arrival_airport = StringField(label='Arrrival Airport', 
                                  validators=[DataRequired(), 
                                              Regexp('^[A-Z]{3}$', message="Must use IATA code format")])
    departure_date = DateField(label='Departure Date', format='%m/%d/%Y', id='datepick', validators=[DataRequired()])
    airline = SelectField(label='Airline', choices = AIRLINES, validators=[DataRequired()])
    submit = SubmitField('Search')