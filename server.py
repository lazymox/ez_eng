import json
from flask import Flask, request, render_template
from flask_cors import CORS

from db import Database
from flask.json.provider import DefaultJSONProvider

app = Flask(__name__, static_url_path='/front/dist/assets', template_folder='front/dist')
db = Database


class CustomJSONProvider(DefaultJSONProvider):
    sort_keys = False


app.json = CustomJSONProvider(app)
CORS(app, resources='*')
app.debug = True


@app.route('/')
def return_site():
    return render_template('index.html')


@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def users_manager():
    match request.method:
        case 'GET':
            return db.get_all_users()
        case 'POST':
            data = request.get_json()
            print(data)
            db.update_data(data, 'users')
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        case 'DELETE':
            print(request.get_json())
            db.delete_user(request.get_json())
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/completed', methods=['GET', 'POST', 'DELETE'])
def completed_manager():
    match request.method:
        case 'GET':
            return db.get_completed_data()
        case 'POST':
            data = request.get_json()
            print(data)
            db.update_data(data, 'completed')
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        case 'DELETE':
            print(request.get_json())
            db.delete_user(request.get_json(), 'completed')
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/payments', methods=['GET', 'POST', 'DELETE'])
def payments_manager():
    match request.method:
        case 'GET':
            return db.get_payments()
        case 'POST':
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        case 'DELETE':
            print(request.get_json())
            db.delete_user(request.get_json(), 'payments')
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run()
