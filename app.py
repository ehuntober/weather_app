
# from crypt import methods
from flask import Flask, redirect, render_template, request, url_for
import json
import urllib.request

import os

from dotenv import load_dotenv

app = Flask('__name__')



class User:
    def __init__(self, name, city):
        self.name = name
        self.city = city

    def __repr__(self):
        return f"{self.name} , {self.city}"


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/details', methods=['GET','POST'])
def details():
    if request.method == "POST":
        name = request.form['name']
        city = request.form['city']
        global user
        user = User(name,city)
        return redirect(url_for('report'))
   
        # return redirect(url_for('report'))
       
    return render_template('details.html')


@app.route('/report', methods=['GET','POST'])
def report():

    city = user.city

    api = os.getenv("api")


    source = urllib.request.urlopen(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}").read()
    list_of_data = json.loads(source)


 
    data = {
        "country_code": str(list_of_data['sys']['country']),
        "coordinate": str(list_of_data['coord']['lon']) + ' ' 
                    + str(list_of_data['coord']['lat']),
        "temp": str(list_of_data['main']['temp']) + 'k',
        "pressure": str(list_of_data['main']['pressure']),
        "humidity": str(list_of_data['main']['humidity']),
    }  
    return render_template('report.html', user = user, data = data)

   
# @app.route('/demo')
# def demo():
#     return render_template('demo.html',user = user)