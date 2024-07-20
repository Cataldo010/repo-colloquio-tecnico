from flask import Flask, request, jsonify
from flask_serverless import Serverless
import boto3 
import os

# Creo un'istanza di Flask e di Serverless
app = Flask(__name__)
serverless = Serverless(app)

# Per poter accedere a DynamoDB ho in precedenza installato la CLI di aws ed eseguito il 
# command aws config in cui ho inserito le credenziali di accesso

# Ho recuperato le credenziali precedentemente inserito nella CLI di aws
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
aws_region_name = os.environ.get('AWS_REGION_NAME')

# Creazione del cliente DynamoDB con i dati di accesso del ruolo IAM associato al DB
dynamodb_client = boto3.client(
    'dynamodb',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region_name
)

# Recupero il nome della tabella che verra usata nelle api del file serverless.ylm
USERS_TABLE = os.environ['USERS_TABLE']
user_table = dynamodb_client.Table(USERS_TABLE)

# Registro le route '/', '/users', '/users/user_id'

# Ho creato questa route per testare il corretto funzionamento 
@app.route('/')
def index():
    return jsonify({'message': 'Hello Serverless'}), 201

# Route che contiene l'api per la creazione di un nuovo user
@app.route('/users', methods=['POST'])
def create_user():
    # Salvo il file .json che mi arriva a questo endpoint
    user_data = request.get_json()
    # Inserisco nella tabella il documento che mi è arrivato
    user_table.put_item(Item=user_data)
    return jsonify({'message': 'User created successfully'}), 201

# Route che contiene l'api per il recupero di un user tramite l'user_id
@app.route('/users/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    # Recupero l'user dalla tabella tramite la ricerca per user_id
    response = user_table.get_item(Key={'user_id': user_id})

    # Se viene trovato qualcosa allora procedo a stampare il json contenete la risposta
    if 'Item' in response:
        return jsonify(response['Item']), 200
    # Se non viene trovato qualcosa verrà visualizzato un messaggio per riferire che non è stato trovato alcun user  
    else:
        return jsonify({'message': 'User not found'}), 404

serverless.wsgi_app = app