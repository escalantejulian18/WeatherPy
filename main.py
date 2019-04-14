# -*- coding: utf-8 -*-
from pymongo import MongoClient
from flask import Flask, jsonify, render_template,request,redirect,url_for
# from bson.json_util import dumps
import requests


def get_db_connection(uri):
    client = MongoClient(uri)
    return client.weatherai

app = Flask(__name__)

connection = get_db_connection('mongodb://localhost:27017/')

@app.route("/")
@app.route("/list")
def get_documents():
    documents = connection.data.find()
    # print(documents)
    return render_template('list.html', documents = documents)

def get_json():
    r = requests.get("http://api.wunderground.com/api/14e789d95869eb26/astronomy/conditions/q/argentina/concepcion%20del%20uruguay.json")
    #r = requests.get("http://api.wunderground.com/api/7e752dc33565333f/astronomy/conditions/q/-32.4824900,-58.2372200.json")
    # URL del Json) # solicitud para extraer el json de la url con requests
    if r.status_code == 200: # ¿respuesta? 200: ok
        result = r.json() # asignamos el json
        connection.data.insert(result)
        return result # devolvemos el json resultante
    raise Exception('API Error') # error de solicitud

@app.route('/sample')
def sample():
    document = get_json()
    return render_template('sample.html',
                                        city = document['current_observation']['display_location']['full'],
                                        weather = document['current_observation']['weather'],
                                        icon = document['current_observation']['icon_url'],
                                        temp = document['current_observation']['temp_c'],
                                        humidity = document['current_observation']['relative_humidity'],
                                        pressure = document['current_observation']['pressure_mb'],
                                        dewpoint = document['current_observation']['dewpoint_c'],
                                        visibility = document['current_observation']['visibility_km'],
                                        precip = document['current_observation']['precip_1hr_string'],
                                        headindex = document['current_observation']['heat_index_c'],
                                        feelslike = document['current_observation']['feelslike_c'],
                                        wind = document['current_observation']['wind_kph'],
                                        wind_dir = document['current_observation']['wind_dir']

                            )
@app.route('/j48')
def j48():
    import j48
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
