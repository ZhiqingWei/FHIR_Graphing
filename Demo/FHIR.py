import requests
import Patient as Patient

class FHIR_response():
    
    def __init__(self):
        self.__CLIENT_ID = "0f6332f4-c060-49fc-bcf6-548982d56569"
        self.__CLIENT_SECRET = "ux@CJAaxCD85A9psm-Wdb?x3/Z4c6gp9"
        self.__SCOPE = "https://gosh-fhir-synth.azurehealthcareapis.com/.default"
        self.__FHIR_BASE_URL = "https://gosh-fhir-synth.azurehealthcareapis.com"
        self.__payload = "grant_type=client_credentials&client_id={}&client_secret={}&scope={}".format(self.__CLIENT_ID, self.__CLIENT_SECRET, self.__SCOPE)
        self.__url = "https://login.microsoftonline.com/ca254449-06ec-4e1d-a3c9-f8b84e2afe3f/oauth2/v2.0/token"
        self.__headers = { 'content-type': "application/x-www-form-urlencoded" }
        self.__access_token = self.get_access_token()
        self.__auth_header = self.make_auth_header(self.__access_token)

    def get_access_token(self):
        res = requests.post(self.__url, self.__payload, headers=self.__headers)
        if res.status_code == 200:
            response_json = res.json()
            return response_json.get('access_token', None)

    def make_auth_header(self, access_token):
        return {'Authorization': 'Bearer {}'.format(access_token), 'Content-Type':'application/fhir+json'}

    def get_all_patients(self):
        res = requests.get('{}/Patient'.format(self.__FHIR_BASE_URL), headers=self.__auth_header)
        json = res.json()
        result = self.__get_all_patients_page(json, [])

        patients = []
        for patient_json_data in result:
            for patient_data in patient_json_data["entry"]:
                patients.append(Patient.Parse_Patient().verify_json(patient_data))
        print(len(patients))
        return patients

    
    def __get_all_patients_page(self, json, list):
        if (json == None):
            return 

        relation = json["link"][0]["relation"]
        list.append(json)

        if (relation == "next"):
            url = json["link"][0]["url"]
            res = requests.get(url, headers=self.__auth_header)
            json = res.json()
            return self.__get_all_patients_page(json, list)
        else:
            return list
        

    # def get_Observation(self,id):
    #     res = requests.get('{}/Observation?patient={}'.format(self.__FHIR_BASE_URL, id), headers=self.__auth_header)
    #     json = res.json()
    #     result = self.__get_patient_all_observations(json, [])

    #     observations = []
    #     for observation_bundle in observations:
    #         for observation in observation_bundle["entry"]:
    #             observations.append()
        
    #     return observations
    
    # def __get_patient_all_observations(self, json, list):
    #     if (json == None):
    #         return 

    #     relation = json["link"][0]["relation"]
    #     list.append(json)

    #     if (relation == "next"):
    #         url = json["link"][0]["url"]
    #         res = requests.get(url, headers=self.__auth_header)
    #         json = res.json()
    #         return self.__get_patient_all_observations(json, list)
    #     else:
    #         return list


