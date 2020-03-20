# FHIR_Graph

Welcome to FHIR_Graph API!

This returns two kinds of graph: 
  
  1. **Geo distribution** as *scattered dot* graph
  
  2. **Age-gender distribution** as *stacked bar chart* graph
  
...and data is available to be downloaded in either **csv** or **xml** format!

## Get Started
  
  * Clone the project and open it in Visual Studio Code.
  
  * `pip install -r requirements.txt`
  
    **API folder**: Contain the **GraphingAPI.py** with a *requirements.txt*
  
    **Demo folder**: Contain a webAPI-like demo for the FHIR_Graph API with a *requirements.txt*
    
## Running the demonstrator

  * Navigate to Demo folder using `cd Demo`
  
  * Run the *Demo.py* in command line using `python Demo.py`
  
  * Open a web browser and go to http://127.0.0.1:5002/ to start
  
## Available API endpoints
  
  | Geo distribution |
  | --- |
  | `GET`  */api/patients_geo/graph* |
  | `GET`  */api/patients_geo/csv* |
  | `GET`  */api/patients_geo/xml* |
  
  
  | Age distribution |
  | --- |
  | `GET`  */api/patients_age/graph* |
  | `GET`  */api/patients_age/csv* |
