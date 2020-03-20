import json
from datetime import datetime

class Address():
        def __init__(self, latitude:float=0.0, longitude:float=0.0, line=[], city="", state="", postalCode="", country=""):
            self.latitude = latitude
            self.longitude = longitude
            self.line = line
            self.city = city
            self.state = state
            self.postalCode = postalCode
            self.country = country


class Patient():

    def __init__(self):
        self.id = ""
        self.name = None
        self.telecom = None
        self.gender = ""
        self.birth_date = None
        self.address = None
        self.marital_status = None
        self.multiple_birth = False
        self.communication = None
        self.extensions = None
        self.identifiers = None

class Parse_Patient():

    def __init__(self):
        self.Patient = Patient()

    def generate_Address(self, address_array):
        for i in range (0, len(address_array)):
            json_address = address_array[i]
            address_object = Address()
            
            try:
                latitude_object = json_address["extension"][0]["extension"][0]
                if (latitude_object["url"] == "latitude"):
                    address_object.latitude = latitude_object["valueDecimal"]

                longitude_object = json_address["extension"][0]["extension"][1]
                if (longitude_object["url"] == "longitude"):
                    address_object.longitude = longitude_object["valueDecimal"]
            except KeyError:
                pass
            
            try:
                address_object.line = json_address["line"]
            except KeyError:
                pass

            try:
                address_object.city = json_address["city"]
            except KeyError:
                pass

            try:
                address_object.state = json_address["state"]
            except KeyError:
                pass

            try:
                address_object.country = json_address["country"]
            except KeyError:
                pass

            try:
                address_object.postalCode = json_address["postalCode"]
            except KeyError:
                pass

            self.Patient.address = address_object
            
    def generate_DOB(self, dob):
        p_dob = datetime.strptime(dob, '%Y-%m-%d')
        self.Patient.birth_date = p_dob

    def verify_json(self, json_to_verify):
        full_url = json_to_verify["fullUrl"]
        resources = json_to_verify["resource"]
        if (isinstance(full_url, str) and (resources is not None)):
            if (resources["resourceType"] == "Patient"):
                try:
                    self.Patient.id = resources["id"]
                except KeyError:
                    pass

                try:
                    self.Patient.gender = resources["gender"]
                except KeyError:
                    pass
                    
                try:
                    self.generate_Address(resources["address"])
                except KeyError:
                    pass

                try:
                    self.generate_DOB(resources["birthDate"])
                except KeyError:
                    pass

        return self.Patient
        

