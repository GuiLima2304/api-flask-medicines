from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_cors import CORS
import test


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
    def get(self):
        conn = db_connect_drugs.connect()
        query = conn.execute("select * from drugs")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def post(self):
        conn = db_connect_drugs.connect()
        primary_drug = request.json['primary_drug']
        second_drug = request.json['second_drug']
        
        resultadoMedicamento1 = test.teste(primary_drug)
        resultadoMedicamento2 = test.teste(second_drug)

        listMedicamentos.clear()
        listMedicamentos.append(resultadoMedicamento1)
        listMedicamentos.append(resultadoMedicamento2)

        conn.execute(
            "insert into drugs values(null, '{0}','{1}')".format(primary_drug, second_drug))

        query = conn.execute('select * from drugs order by id desc limit 1')
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        return jsonify(listMedicamentos)

api.add_resource(Medicamentos, '/medicines')

if __name__ == '__main__':
    app.run()

