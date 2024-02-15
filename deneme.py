"""
@prefix wot: <http://xmlns.com/wot/0.1/> .
@prefix core: <http://iot.linkeddata.es/def/core#> .
@prefix ex: <http://example.org/> .
@prefix map: <http://iot.linkeddata.es/def/wot-mappings#> .
@prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:TemperatureSensor01 a wot:Thing ;
                      a core:Thermometer ;
                      wot:thingName "Temperature Sensor 01" .

ex:TemperatureSensor01TD a core:ThingDescription ;
                          core:describes ex:TemperatureSensor01 ;
                          map:hasAccessMapping ex:TemperatureSensor01TD-AM1 .

ex:TemperatureSensor01TD-AM1 a map:AccessMapping ;
                              map:mapsResourcesFrom ex:TemperatureSensor01-AM1-Link1 ;
                              map:hasMapping ex:mapping1, ex:mapping2 .

ex:TemperatureSensor01-AM1-Link1 a wot:Link ;
                                   wot:href "http://localhost" ;
                                   wot:hasMediaType "application/json" .

ex:mapping1 a map:Mapping ;
            map:predicate geo:lat ;
            map:key "latitude"^^xsd:string .

ex:mapping2 a map:Mapping ;
            map:predicate geo:long ;
            map:key "longitude"^^xsd:string .
"""
"""
{
  "@context": {
    "wot": "http://xmlns.com/wot/0.1/",
    "core": "http://iot.linkeddata.es/def/core#",
    "ex": "http://example.org/",
    "map": "http://iot.linkeddata.es/def/wot-mappings#",
    "geo": "http://www.w3.org/2003/01/geo/wgs84_pos#",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@id": "ex:TemperatureSensor01",
  "@type": [
    "wot:Thing",
    "core:Thermometer"
  ],
  "wot:thingName": "Temperature Sensor 01",
  "ex:TemperatureSensor01TD": {
    "@type": "core:ThingDescription",
    "core:describes": "ex:TemperatureSensor01",
    "map:hasAccessMapping": "ex:TemperatureSensor01TD-AM1"
  },
  "ex:TemperatureSensor01TD-AM1": {
    "@type": "map:AccessMapping",
    "map:mapsResourcesFrom": "ex:TemperatureSensor01-AM1-Link1",
    "map:hasMapping": [
      "ex:mapping1",
      "ex:mapping2"
    ]
  },
  "ex:TemperatureSensor01-AM1-Link1": {
    "@type": "wot:Link",
    "wot:href": "http://localhost",
    "wot:hasMediaType": "application/json"
  },
  "ex:mapping1": {
    "@type": "map:Mapping",
    "map:predicate": "geo:lat",
    "map:key": "latitude"
  },
  "ex:mapping2": {
    "@type": "map:Mapping",
    "map:predicate": "geo:long",
    "map:key": "longitude"
  }
}

"""
import requests
import json
from rdflib import Graph, URIRef, Literal, Namespace

g = Graph()

wot = Namespace("http://xmlns.com/wot/0.1/")
geo = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
ex = Namespace("http://example.org/")

td_uri = "http://example.org/TemperatureSensor01TD"
response = requests.get(td_uri)
td_data = json.loads(response.text)

for link in td_data["links"]:
    if link["href"]:
        endpoint_href = link["href"]
        # Endpoint
        response = requests.get(endpoint_href)
        endpoint_data = json.loads(response.text)
        # JSON to RDF
        for mapping in endpoint_data["mappings"]:
            predicate = mapping["predicate"]
            key = mapping["key"]
            value = mapping["value"]
            if predicate == "geo:lat" or predicate == "geo:long":
                value_literal = Literal(value, datatype=xsd.float)
            else:
                value_literal = Literal(value)
            g.add((td_uri, URIRef(predicate), value_literal))

print(g.serialize(format="turtle").decode())