#!/usr/bin/env python

import datetime
from flask import Flask, render_template, request, flash, redirect, url_for
from google.auth.transport import requests
from google.cloud import datastore
import google.oauth2.id_token
from pprint import pprint as pp

from weather import query_api

app = Flask(__name__)
#firebase_request_adapter = requests.Request()
datastore_client = datastore.Client()



def store_data(dt, data, city):
    entity = datastore.Entity(key=datastore_client.key('weather'))
    entity.update({
        'timestamp': dt,
        'response': data,
        'city': city
    })

    datastore_client.put(entity)


def fetch_data(limit, city):
    query = datastore_client.query(kind='weather')
    query.add_filter("city", "=", city)
    query.order = ['-timestamp']


    results = list(query.fetch(limit=limit))
    print(results)

    return results



@app.route('/')
def index():
    # Store the current access time in Datastore.
    #store_time(datetime.datetime.now())

    # Fetch the most recent 10 access times from Datastore.
    #times = fetch_times(10)


    return render_template('weather.html', data=[{'name':'Toronto'},
                                                 {'name':'Montreal'},
                                                 {'name':'Calgary'},
                                                 {'name':'Ottawa'},
                                                 {'name':'Edmonton'},
                                                 {'name':'Mississauga'},
                                                 {'name':'Winnipeg'},
                                                 {'name':'Vancouver'},
                                                 {'name':'Brampton'},
                                                 {'name':'Quebec'}
                                                 ])

@app.route("/result" , methods=['GET', 'POST'])
def result():
    data = []
    error = None
    select = request.form.get('comp_select')
    print(select)
    resp = query_api(select)
    pp(resp)

    if resp:
        store_data(datetime.datetime.now(), resp, select)
        print("stored entity")
    else:
        print('no response from API')
        error = 'Bad Response from Weather API'

    data = fetch_data(10, select)


    return render_template('result.html', data=data, error=error)


if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8080, debug=True)