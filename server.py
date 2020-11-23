from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_cors import CORS
import crawler


db_connect_drugs = create_engine('sqlite:///medicines.db')
listMedicamentos = []

app = Flask(__name__)
api = Api(app)
CORS(app)

@app.route('/ajax_ddl')
def ajax_ddl(text):
    xml = text
    return Response(xml, mimetype='text/xml')


class Medicamentos(Resource):
    def post(self):
        primary_drug = request.json['primary_drug']
        second_drug = request.json['second_drug']
        
        resultadoMedicamento1 = crawler.GetBula(primary_drug)
        resultadoMedicamento2 = crawler.GetBula(second_drug)

        listMedicamentos.clear()
        listMedicamentos.append(resultadoMedicamento1)
        listMedicamentos.append(resultadoMedicamento2)

        return jsonify(listMedicamentos)

api.add_resource(Medicamentos, '/medicines')

if __name__ == '__main__':
    app.run()

