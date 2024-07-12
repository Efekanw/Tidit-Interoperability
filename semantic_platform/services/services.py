import json
import os
import requests
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from rdflib import Graph, plugin
from SPARQLWrapper import SPARQLWrapper, JSON, POST, SPARQLExceptions

app = Flask(__name__)
api = Api(app, version='1.0', title='Tidit Interoperability API', description='A simple API to interact with a triple store')
ns = api.namespace('tidit interoperability', description='Operations related to triple store')

endpoint_url = 'http://localhost:3030/tidit/'

url_query = endpoint_url + 'sparql'
url_update = endpoint_url + 'update'

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type='FileStorage', required=True)


sparql_model = api.model('SPARQL', {
    'query': fields.String(required=True, description='SPARQL query')
})
thing_model = api.model('ThingModel', {
    'thingid': fields.String(required=True, description='ID of the thing')
})


CA_CERT = './rootCA.crt'
HOST = '172.16.21.127'
PORT = 8883

results = {
    'Voltage': ('', ''),
    'Current': ('', ''),
    'ActivePower': ('', ''),
    'ReactivePower': ('', ''),
    'ApparentPower': ('', ''),
    'PowerFactor': ('', ''),
    'Frequency': ('', '')
}


@ns.route('/register')
class LoadJSONLD(Resource):
    @ns.doc('Register', description='Register thing description with Jsonld')
    @api.expect(upload_parser)
    def post(self):
        uploaded_file = request.files['file']
        try:
            sparql = SPARQLWrapper(url_update)
            print(url_update)
            sparql.setCredentials('admin', 'VLmJN7HfFDAOrNI')

            jsonld_content = json.loads(uploaded_file.read())
            print(jsonld_content)
            g = Graph()
            g.parse(data=jsonld_content, format='json-ld')

            sparql.method = POST
            sparql.setQuery("""
                INSERT DATA {
                    %s
                }
            """ % g.serialize(format='nt'))
            sparql.query()
            return {'message': 'File stored successfully', 'jsonld_content': jsonld_content}, 200
        except json.JSONDecodeError as e:
            return {'message': 'Invalid JSON content in file'}, 400
        except SPARQLExceptions.Unauthorized:
            return {'message': 'Unauthorized: Access to the endpoint is denied due to invalid credentials.'}, 401
        except SPARQLExceptions.QueryBadFormed:
            return {'message': 'Badly formed SPARQL query.'}, 400
        except SPARQLExceptions.EndPointNotFound:
            return {'message': 'SPARQL endpoint not found.'}, 404
        except SPARQLExceptions.EndPointInternalError:
            return {'message': 'Internal server error occurred at the SPARQL endpoint.'}, 500
        except Exception as e:
            return {'message': 'An error occurred while executing the SPARQL query: {}'.format(str(e))}, 500


@ns.route('/discover')
class DiscoverTripleStore(Resource):
    @ns.doc('Discover', description='Discover thing descriptions with Sparql file')
    @api.expect(upload_parser)
    def post(self):
        try:
            query_file = request.files['file']
            query = query_file.read()
            print(query)

            sparql = SPARQLWrapper(url_query)
            sparql.setCredentials('admin', 'VLmJN7HfFDAOrNI')

            sparql.setMethod("POST")
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            print(results)
            return {'message': 'File stored successfully', 'result': results}, 200
        except SPARQLExceptions.Unauthorized:
            return {'message': 'Unauthorized: Access to the endpoint is denied due to invalid credentials.'}, 401
        except SPARQLExceptions.QueryBadFormed:
            return {'message': 'Badly formed SPARQL query.'}, 400
        except SPARQLExceptions.EndPointNotFound:
            return {'message': 'SPARQL endpoint not found.'}, 404
        except SPARQLExceptions.EndPointInternalError:
            return {'message': 'Internal server error occurred at the SPARQL endpoint.'}, 500
        except Exception as e:
            return {'message': 'An error occurred while executing the SPARQL query: {}'.format(str(e))}, 500


@ns.route('/get_data/http')
class GetData(Resource):
    @ns.doc('Get data of thing description', description='Get data of thing description with thing id')
    @api.expect(thing_model)
    def post(self):
        try:
            data = api.payload
            thing_id = data['thingid']
            links = query_by_thing_id(thing_id)
            cleaned_thing_id = thing_id.strip('<>').strip()
            titles = []
            link_list = []
            for entry in links['results']['bindings']:
                titles.append(entry['title']['value'])
                link_list.append(entry['linkValue']['value'])
            results = {}
            for link in link_list:
                request_link = cleaned_thing_id + link
                response = requests.get(request_link, headers={'Accept': 'application/json'})
                if response.status_code == 200:
                    results[link] = response.json()
            print(results)
            return results, 200
        except Exception as e:
            return {"error": str(e)}, 500


def print_table(payload):
    global i
    i += 1
    key = list(payload.keys())[0]
    value = payload[key]['value']
    timestamp = payload[key]['timestamp']
    results[key] = (value, timestamp)
    if i%7 == 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('-'*60)
        print(f'| {"Measurment":<20} | {"Value":<10} | {"Time":<20} |')
        print('='*60)
        for key, val in results.items():
            print(f'| {key:<20} | {val[0]:<10} | {val[1]:<20} |')
            print('-'*60)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Connection failed")


def on_message(client, userdata, message):
    payload = str(message.payload.decode('utf-8'))
    payload = json.loads(payload)
    print_table(payload)


def query_by_thing_id(thing_id):
    query = """
    PREFIX td: <https://www.w3.org/2019/wot/td#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX wot: <https://www.w3.org/2019/wot/td#>
    PREFIX hypermedia: <https://www.w3.org/2019/wot/hypermedia#>

    SELECT DISTINCT ?title ?linkValue
    WHERE {
        id rdf:type wot:Thing ;
        {
          ?thing td:hasActionAffordance ?action .
          ?action td:title ?title ;
                  td:hasLink ?link .
          ?link hypermedia:hasTarget ?linkValue .
        }
      UNION
        {
          ?thing td:hasPropertyAffordance ?property .
          ?property td:title ?title ;
                    td:hasLink ?link .
          ?link hypermedia:hasTarget ?linkValue .
        }
      UNION
        {
          ?thing td:hasEventAffordance ?event .
          ?event td:title ?title ;
                 td:hasLink ?link .
          ?link hypermedia:hasTarget ?linkValue .
        }
    }

    """
    query = query.replace("id", thing_id)
    print(query)
    sparql = SPARQLWrapper(url_query)
    sparql.setCredentials('admin', 'VLmJN7HfFDAOrNI')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return results


if __name__ == '__main__':
    app.run(debug=True)
