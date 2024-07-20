from flask import Flask, request, jsonify
from flask_serverless import Serverless
import boto3 
import os

aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
aws_region_name = os.environ.get('AWS_REGION_NAME')

dynamodb_client = boto3.client(
    'dynamodb',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region_name
)

USERS_TABLE = os.environ['USERS_TABLE']

app = Flask(__name__)
serverless = Serverless(app)

user_table = dynamodb_client.Table(USERS_TABLE)

@app.route('/')
def index():
    return jsonify({'message': 'Hello Serverless'}), 201

@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.get_json()
    user_table.put_item(Item=user_data)
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    response = user_table.get_item(Key={'user_id': user_id})
    if 'Item' in response:
        return jsonify(response['Item']), 200
    else:
        return jsonify({'message': 'User not found'}), 404

serverless.wsgi_app = app