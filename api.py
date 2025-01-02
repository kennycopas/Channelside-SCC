from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import boto3

db = boto3.resource('dynamodb')
table = db.Table('EmployeeData')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

users = {
    'user1': 'password1',
    'user2': 'password2'
}

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if users.get(username) == password:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 401


@app.route('/api', methods=['GET'])
def get_data():
    try:
        id = request.args.get('id')
        response = table.get_item(Key={'EmployeeID': id})
        if 'Item' in response:
            item = response['Item']
            return item
        else:
            return "Item not found"
    except Exception as e:
        return f"Error retrieving item: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)