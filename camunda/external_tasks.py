{
  "@context": ["https://www.w3.org/2019/wot/td/v1", {"sd": "http://bimerr.iot.linkeddata.es/def/sensor-data#", "saref": "https://saref.etsi.org/core/"}],
  "@type": "Thing",
  "title": "SensorThing",
  "description": "A sensor represented using WoT TD and linked to the Sensor Data ontology.",
  "properties": {
    "baseName": {
      "type": "string",
      "readOnly": true,
      "description": "A string that is prepended to the names found in the records."
    },
    "baseSum": {
      "type": "number",
      "readOnly": true,
      "description": "A base sum is added to the sum found in a record."
    },
    "baseTime": {
      "type": "number",
      "readOnly": true,
      "description": "A base time that is added to the time found in a record."
    },
    "baseValue": {
      "type": "number",
      "readOnly": true,
      "description": "A base value is added to the value found in a record."
    },
    "baseVersion": {
      "type": "integer",
      "readOnly": true,
      "description": "Version number of the media type format."
    },
    "name": {
      "type": "string",
      "readOnly": true,
      "description": "Name of the sensor or parameter."
    },
    "sum": {
      "type": "number",
      "readOnly": true,
      "description": "Integrated sum of the values over time."
    },
    "time": {
      "type": "number",
      "readOnly": true,
      "description": "Time when the value was recorded."
    },
    "updateTime": {
      "type": "number",
      "readOnly": true,
      "description": "Period of time in seconds that represents the maximum time before this sensor will provide an updated reading for a measurement."
    },
    "hasValue": {
      "type": "number",
      "readOnly": true,
      "description": "A relationship defining the value of a certain property."
    }
  },
  "securityDefinitions": {
    "nosec_sc": {
      "scheme": "nosec"
    }
  }
}
