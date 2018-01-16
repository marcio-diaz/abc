import sqlite3
from flask import Flask, g
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

DATABASE = 'predictions.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

class CustomerPrediction(Resource):
    def get(self, customer_id):
        query_str = 'select * from predictions where customer_id = ?'
        prediction = query_db(query_str, [customer_id], one=True)
        if not prediction:
            return "Invalid customer_id."
        return prediction[2]

api.add_resource(CustomerPrediction, '/<string:customer_id>')

if __name__ == '__main__':
    app.run(debug=True)
