from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_cors import CORS
import test

db_connect_drugs = create_engine('sqlite:///medicines.db')

app = Flask(__name__)
api = Api(app)
CORS(app)


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

        conn.execute(
            "insert into drugs values(null, '{0}','{1}')".format(primary_drug, second_drug))

        query = conn.execute('select * from drugs order by id desc limit 1')
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(resultadoMedicamento1, resultadoMedicamento2)

api.add_resource(Medicamentos, '/medicines')

if __name__ == '__main__':
    app.run()

