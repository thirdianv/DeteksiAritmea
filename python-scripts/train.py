from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS  # Import the CORS module
import pandas as pd
from train_model_script import train_and_save_models
from io import BytesIO

import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/train-model', methods=['POST'])
def train_model():
    try:
        # file_data = request.json['file']
        file_data = request.json
        decoded_file = base64.b64decode(file_data['file'])

        # Convert the file content to a DataFrame (assuming CSV format)
        # df = pd.read_excel(StringIO(decoded_file.decode('utf-8')))
        df = pd.read_excel(BytesIO(decoded_file))

        # Call the training function
        # train_and_save_models(df, label='Label', model_save_path='./models')


        accuracy_data = train_and_save_models(df, label='Label', model_save_path='./models')

        # return jsonify({'success': True, 'accuracy': accuracy_data}), 200
        # print("Request processed successfully.")
        response_data = {'success': True, 'accuracy': accuracy_data}
        return jsonify(response_data), 200
    except Exception as e:
        print("Error:", str(e))
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
