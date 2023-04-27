from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# Google Maps API key
GOOGLE_MAPS_API_KEY = 'AIzaSyBYPSqaGxAw2iN83-0zPH25lcB84qw068M'

# US Census Bureau API key
CENSUS_API_KEY = '278e989e44fa95d929981351e4d83aa2676994b3'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit(data):
    address = data['address']
    city = data['city']
    state = data['state']
    county = data['county']

    # Get distance from the new location to Claremont
    url = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins=Claremont%2C%20CA'
    # &destinations={address}%2C{city}&units=imperial&key=AIzaSyBYPSqaGxAw2iN83-0zPH25lcB84qw068M'
    params = {'destinations': f'{address}, {city}, {state}', 'key': GOOGLE_MAPS_API_KEY}
    response = requests.get(url, params=params)
    data = json.loads(response.text)
    distance = data['rows'][0]['elements']['distance']['value']

    # Get income data from US Census Bureau API
    url = f'https://api.census.gov/data/2019/acs/acs5/profile?get=DP03_0052E&for=county:{county}&in=state:{state}&key={CENSUS_API_KEY}'
    response = requests.get(url)
    data = json.loads(response.text)
    income = data[1][0]

    # Store location, miles travelled, and income in a text file
    with open('data.txt', 'a') as file:
        file.write(f'{address}, {city}, {state}, {county}, {income}\n')

    return render_template('index.html', message='Data submitted successfully!')

if __name__ == '__main__':
    app.run(debug=True)
