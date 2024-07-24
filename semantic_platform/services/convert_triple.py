import requests
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, XSD


def convert(thing_id, id, data, datatype, time, counter, triple_type):
    SOSA = Namespace("https://www.w3.org/ns/sosa#")
    WOT = Namespace("https://www.w3.org/2019/wot/td#")
    CDT = Namespace("http://w3id.org/def/ucum#")
    SSN = Namespace("http://www.w3.org/ns/ssn/")

    g = Graph()
    print(SOSA)
    g.bind("sosa", SOSA)
    g.bind("wot", WOT)
    g.bind("cdt", CDT)
    g.bind("xsd", XSD)
    g.bind('ssn', SSN)

    thing_uri = URIRef(thing_id)
    property_uri = URIRef(id)
    observation_uri = URIRef(f"{id}/Observation/{counter}")
    if datatype == 'float':
        datatype = XSD.float
    elif datatype == 'boolean':
        datatype = XSD.boolean
    g.add((thing_uri, RDF.type, SOSA.Sensor))
    g.add((thing_uri, SOSA.observes, property_uri))
    print(SOSA.Observation)
    pao = ''
    if triple_type == 'p':
        pao = SOSA.observedProperty
    elif triple_type == 'e':
        pao = SSN.detects
    g.add((observation_uri, RDF.type, SOSA.Observation))
    g.add((observation_uri, pao, property_uri))
    g.add((observation_uri, SOSA.madeBySensor, thing_uri))
    g.add((observation_uri, SOSA.hasSimpleResult, Literal(data, datatype=datatype)))
    g.add((observation_uri, SOSA.resultTime, Literal(time, datatype=XSD.dateTime)))

    return g


def insert_into_fuseki(graph, fuseki_url, username, password):
    data = graph.serialize(format='turtle')

    url = f"{fuseki_url}data"

    headers = {
        'Content-Type': 'text/turtle'
    }
    auth = (username, password)

    try:
        response = requests.post(url, data=data, headers=headers, auth=auth)
        response.raise_for_status()

        print("Data successfully inserted into FUSEKI")

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            print("Unauthorized: Invalid credentials.")
        else:
            print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")