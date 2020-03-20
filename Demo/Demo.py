import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'API'))
from flask import Flask, redirect, request, Response

from FHIR import FHIR_response
from GraphingAPI import *

app = Flask(__name__)

_fhir = FHIR_response()
_data = _fhir.get_all_patients()

@app.route('/')
def index():
    return """
    <h1> Simple FHIR Graphing API demo </h1>
    """

@app.route('/api/patients_geo/csv', methods=['GET'])
def geo_csv():
    if (Patient_Geo_csv(_data)):
        return """
        <h3> CSV download successful! </h3>
        """
    else:
        return "CSV download unsuccessful."

@app.route('/api/patients_geo/xml', methods=['GET'])
def geo_xml():
    if (Patient_Geo_xml(_data)):
        return """
        <h3> XML download successful! </h3>
        """
    else:
        return "XML download unsuccessful."

@app.route('/api/patients_geo/graph', methods=['GET'])
def geo_graph():
    Patient_Geo_graph(_data)
    return "Graph shown in new tab."

@app.route('/api/patients_age/csv', methods=['GET'])
def age_csv():
    if (Patient_AgeGender_csv(_data)):
        return """
        <h3> CSV download successful! </h3>
        """
    else:
        return "CSV download unsuccessful."

@app.route('/api/patients_age/graph', methods=['GET'])
def age_graph():
    Patient_AgeGender_graph(_data)
    return "Graph shown in new tab."


if __name__ == '__main__':
    app.run(port='5002', debug=True)