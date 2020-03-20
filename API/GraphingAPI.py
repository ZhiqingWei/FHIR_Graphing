'''GraphingAPI.py - Tools for graphing FHIR Json data
'''

#Currently supported:
#   1. Graphing age distributuion of patients
#   2. Graphing geo distributuion of patients

__all__ = ['Patient_Geo_graph', 'Patient_Geo_csv', 'Patient_Geo_xml',
           'Patient_AgeGender_graph', 'Patient_AgeGender_csv']

import plotly.express as go
import pandas as pd
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import date

    
_geoLabels = ["Longitude", "Latitude", "State", "City", "Patient_count"]
    
def __xml_prettify(elem):
    """
    Return a pretty-printed XML string for the Element. \n
    Copied from "https://stackoverflow.com/questions/749796/pretty-printing-xml-in-python"
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

#####################################
#######   GEO DISTRIBUTION    #######
#####################################
def __Patient_Geo_Distribution(patients):
    
    W_lon = []
    W_lat = []
    W_states = []
    W_cities = []
    W_count = []
    W_countries = {}

    for patient in patients:
        if (patient.address is not None):
            city = patient.address.city
            if (city not in W_cities):
                W_cities.append(city)
                W_lon.append(patient.address.longitude)
                W_lat.append(patient.address.latitude)
                W_states.append(patient.address.state)
                W_count.append(1)
            else:
                W_count[W_cities.index(city)] += 1
                W_lon[W_cities.index(city)] += patient.address.longitude
                W_lat[W_cities.index(city)] += patient.address.latitude
            
            if (W_countries.get(patient.address.state) == None):
                W_countries.update({patient.address.state : patient.address.country})

    # print("Lon length: ", len(US_lon))
    # print("Lat length: ", len(US_lat))
    # print("State length: ", len(US_states))
    # print("Cities length: ", len(US_cities))
    # print("Count length: ", len(US_count))

    dict = {_geoLabels[0]: W_lon, 
            _geoLabels[1]: W_lat, 
            _geoLabels[2]: W_states,
            _geoLabels[3]: W_cities, 
            _geoLabels[4]: W_count}
    
    df = pd.DataFrame.from_dict(dict)
    df["Longitude"] = df["Longitude"] / df["Patient_count"]
    df["Latitude"] = df["Latitude"] / df["Patient_count"]
    return df, W_countries

def Patient_Geo_graph(patients):
    """
    Taking in list of patient objects and produce SCATTER diagram on world map.
    
    @param patients : list of patient objects
    """

    df, _ = __Patient_Geo_Distribution(patients)
    df["text"] = df["City"]+' Patient counts: '+df["Patient_count"].astype(str)

    fig = go.scatter_geo(
        df,
        lon="Longitude",
        lat="Latitude",
        hover_name="City",
        color="Patient_count",
        center={'lon':df["Longitude"].median(), 'lat':df["Latitude"].median()},
        color_continuous_midpoint=df["Patient_count"].mean(),
        color_continuous_scale=go.colors.sequential.Reds,
        title = 'Patient layout'
    )

    fig.show()
    # return fig

def Patient_Geo_csv(patients, path=os.getcwd(), filename="PatientGeo"):
    """
    Taking in list of patient objects and return csv format file.
    
    @param patients : list of patient objects \n
    @param path : str \n
    @param filename: str
    """

    try:
        df , _ = __Patient_Geo_Distribution(patients)
        df.to_csv(path_or_buf=open(path+os.sep+filename+".csv", "w"), index=False)
        return 1
    except:
        return 0

def Patient_Geo_xml(patients, path=os.getcwd(), filename="PatientGeo"):
    """
    Taking in list of patient objects and return xml format file.
    
    @param patients : list of patient objects \n
    @param path : str \n
    @param filename: str
    """

    df , country_list = __Patient_Geo_Distribution(patients)
    # print("df shape", df.shape)
    country_dict = {}
    state = {}

    world = ET.Element("world")
    for country_name in set(country_list.values()):
        country_dict.update({country_name : ET.SubElement(world, "country", {'value': country_name})})

    for row in df.itertuples():
        if (state.get(row.State) == None):
            current_state = ET.SubElement(country_dict[country_list[row.State]], "state", {'value': row.State})
            state.update( {row.State : current_state})

        city = ET.SubElement(state[row.State], "city", {'value': row.City})
        city_exten = ET.SubElement(city, "extension", 
                                    {'xmlns': "http://hl7.org/fhir",
                                        'url': "http://hl7.org/fhir/StructureDefinition/geolocation"
                                        })
        city_exten.append(ET.Comment("extension sliced by value:url  in the specified orderOpen"))

        extern_lat = ET.SubElement(city_exten, "extension", {'url': 'latitude'})
        lat_value = ET.SubElement(extern_lat, "valueDecimal", {'value': str(row.Latitude)})
        extern_lon = ET.SubElement(city_exten, "extension", {'url': 'longitude'})
        lat_value = ET.SubElement(extern_lon, "valueDecimal", {'value': str(row.Longitude)})

        patient_count = ET.SubElement(city, "count", {'value': str(row.Patient_count)})
    
    with open(path+os.sep+filename+".xml", "w") as f:
        f.write(__xml_prettify(world))

#####################################
#######   AGE DISTRIBUTION    #######
#####################################
def __Patient_Age_Distribution(patients):

    ages = []
    genders = []
    max_age = 0
    min_age = 1000000

    for patient in patients:
        today = date.today() 
        age = today.year - patient.birth_date.year - ((today.month, today.day) < (patient.birth_date.month, patient.birth_date.day))
        ages.append(age)
        genders.append(patient.gender)

        if (age > max_age):
            max_age = age
        if (age < min_age):
            min_age = age

    interval = (max_age - min_age) // 10
    min_age = min_age - min_age % 10
    intervals = [min_age+(i+1)*10 for i in range (interval-1)]

    interval_length = len(intervals)
    intervals_dict = [{"male": 0, "female": 0} for i in range (interval_length+1)]
    
    for i in range (len(ages)):
        for j in range (interval_length):
            if (j == 0) and (ages[i] < intervals[0]):
                intervals_dict[j][genders[i]] += 1
                break
            elif (ages[i] < intervals[j]) and (ages[i] > intervals[j-1]):
                intervals_dict[j-1][genders[i]] += 1
                break
            elif (j == interval_length-1) and (ages[i] > intervals[j]):
                intervals_dict[interval_length][genders[i]] += 1
                break

    return intervals, intervals_dict

def Patient_AgeGender_graph(patients):
    """
    Taking in list of patient objects and return STACKED BAR chart for age distribution.
    
    @param patients : list of patient objects
    """

    intervals, intervals_dict = __Patient_Age_Distribution(patients)

    length = len(intervals)
    age_label = []
    for i in range (length):
        if (i == 0):
            text = "< "+str(intervals[0])
        else:
            text = str(intervals[i-1])+"-"+str(intervals[i])
        
        age_label.append(text)
        age_label.append(text)
    age_label.append("> "+str(intervals[length-1]))
    age_label.append("> "+str(intervals[length-1]))

    amount = []
    genders = []
    for j in range (len(intervals_dict)):
        amount.append(intervals_dict[j]["female"])
        amount.append(intervals_dict[j]["male"])
        genders.append("female")
        genders.append("male")

    print(len(age_label), len(amount), len(genders))
    df = pd.DataFrame.from_dict(dict(Age_intervals=age_label, Amount=amount, Gender=genders))
    df["Text"] = df["Gender"]+": "+df["Amount"].astype(str)

    fig = go.bar(df, x="Age_intervals", y="Amount", color="Gender", hover_name="Text")
    fig.show()

def __age_gender_dataframe_helper(intervals, intervals_dict):
    length = len(intervals)
    age_label = []
    for i in range (length):
        if (i == 0):
            text = "< "+str(intervals[0])
        else:
            text = str(intervals[i-1])+"-"+str(intervals[i])
        
        age_label.append(text)
    age_label.append("> "+str(intervals[length-1]))

    females = []
    males = []
    for j in range (len(age_label)):
        females.append(intervals_dict[j]["female"])
        males.append(intervals_dict[j]["male"])
    
    df = pd.DataFrame.from_dict(dict(Age_intervals=age_label, Male_amount=males, Female_amount=females))

    return df

def Patient_AgeGender_csv(patients, path=os.getcwd(), filename="PatientAgeDistribution"):
    """
    Taking in list of patient objects and return csv format file for age distribution.
    
    @param patients : list of patient objects \n
    @param path : str \n
    @param filename: str
    """

    intervals, intervals_dict = __Patient_Age_Distribution(patients)
    df = __age_gender_dataframe_helper(intervals, intervals_dict)
    try:
        df.to_csv(path_or_buf=open(path+os.sep+filename+".csv", "w"), index=False)
        return 1
    except:
        return 0
