from flask import Flask, send_file, jsonify, request
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
import requests
import tempfile
import zipfile
import patoolib
import os
import pandas as pd
import matplotlib
matplotlib.use('agg')
import pandas as pd
from train_model_script import train_and_save_models
from joblib import load

app = Flask(__name__)


def extract_compressed_file(file_to_extract, destination_folder):
    folder_name = os.path.splitext(os.path.basename(file_to_extract))[0]  # Ambil nama file tanpa ekstensi

    # Gabungkan folder tujuan dengan nama folder yang dihasilkan dari nama file
    destination_folder = os.path.join(destination_folder, folder_name)

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

        # Eksperimen untuk mengekstrak file ke folder tujuan menggunakan patoolib
    try:
        patoolib.extract_archive(file_to_extract, outdir=destination_folder)
        print(f"File '{file_to_extract}' berhasil diekstrak ke '{destination_folder}'")
        os.remove(file_to_extract)
        return destination_folder
    except patoolib.util.PatoolError as e:
        print(f"Gagal mengekstrak file: {e}")

    return "File berhasil di ekstrak"

def file_check(file_name, folder_path):
    if os.path.exists(os.path.join(folder_path, file_name)):
        path = folder_path + "\\" + file_name
        result = extract_compressed_file(path, folder_path)
        print(result)
        return jsonify({'file_exists': True, 'message': f'File "{path}" ditemukan.'}), 200
    else:
        return jsonify({'file_exists': False, 'message': f'File "{path}" tidak ditemukan.'}), 404

def read_data(file_path):
    df = pd.read_excel(file_path, header=0)
    s1 = df[df.columns[1]]
    return s1

def check_type(file_name):
    # Split the file name using '_' as the separator
    parts = file_name.split('_')

    # Extract the desired part before the underscore
    result = parts[0]
    # Check if the result is 'normal' or 'abnormal'
    if result.lower() == 'normal':
        return 'N'
    elif result.lower() == 'abnormal':
        return 'A'
    else:
        return 'Unknown'
    
import numpy as np
import pyhrv.frequency_domain as fd
import pyhrv.time_domain as td
    
def feature_extraction(data, label='unknown'):
    numeric_data = pd.to_numeric(data, errors='coerce')
    numeric_data = numeric_data.dropna()
    
    mean_value = numeric_data.mean()
    hr_value = 60/mean_value
    std_hr = np.std(numeric_data)
    cvr_value = (std_hr/mean_value*100)
    rmssd_value = np.sqrt(np.mean(np.square(np.diff(numeric_data))))
    
    psd = fd.welch_psd(numeric_data, show = False)
    fd.plt.close()
    
    peakPSD = psd['fft_peak']
    lfPeak_value = peakPSD[1]
    hfPeak_value = peakPSD[2]
    
    normPSD = psd['fft_norm']
    lfNorm_value = normPSD[0]
    hfNorm_value = normPSD[1]
    
    lfhf_value = lfNorm_value/hfNorm_value
    
    _sdsd = td.sdsd(numeric_data)
    _sdsd = _sdsd['sdsd']
    
    _nn50 = td.nn50(numeric_data)
    _nn50 = _nn50['nn50']
    
    td.plt.close()

    return [mean_value, hr_value, std_hr, cvr_value, rmssd_value, _nn50, _sdsd, lfPeak_value, hfPeak_value, lfNorm_value, hfNorm_value, lfhf_value, label]

def empty_df():
    # Dictionary with column names
    new_df = [
        'meanRR', 'HR', 'SDRR', 'CVR', 'RMSSD', 'NN50', 'SDSD', 'LF_Peak', 'HF_Peak', 'LF_Norm', 'HF_Norm', 'LF/HF', 'Label']
    # Convert the set of column names to a list
    columns_list = list(new_df)
    # Create an empty DataFrame with only headers
    new_df = pd.DataFrame(columns=columns_list)
    return new_df

def feature(path, training=True):
    files = os.listdir(path)
    print(files)
    new_df = empty_df()
    for file in files:
        if file.endswith('.xlsx'):
            print("Pengolahan : ", file, "\n")
            data = read_data(os.path.join(path, file))
            label = check_type(file)
            fe = feature_extraction(data, label = label)

            new_df.loc[len(new_df)] = fe
            name = path + '\\' + 'fitur.xlsx'
        else:
            print(file)
    new_df.to_excel(name, index=False)
    return name


@app.route('/api/model', methods=['POST', 'GET'])
def model():
    print('model');
    if 'file_name' not in request.json:
        return jsonify({'error': 'Nama file tidak disediakan'}), 400

    file_name = request.json['file_name']
    folder_path = 'F:\\vicky\\DeteksiAritmea\\storage\\app\\public'  # Ganti dengan path folder Anda
    new_folder = file_check(file_name, folder_path)

    folder_name = os.path.splitext(os.path.basename(file_name))[0]  # Ambil nama file tanpa ekstensi
    destination_folder = os.path.join(folder_path, folder_name)
   
    # feature extraction
    feature_file = feature(destination_folder)

    feature_dict = {
        'feature_name': feature_file,
    }

    print(feature_dict)

    return jsonify(feature_dict)

@app.route('/api/predict-data', methods=['POST'])
def execute_feature_extraction():
    print('\nFeature Extraction.....')
    
    if 'file_path' not in request.json:
        return jsonify({'error': 'File path not provided!'}), 400
    
    file_path = request.json['file_path']
    model_path = request.json['model_path']

    print('file_path :', file_path)
    print('public_path :', model_path)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found!'}), 404

    data = read_data(file_path)

    # Call the feature extraction logic function
    feature_file = feature_extraction(data)
    feature_file = np.array(feature_file[:-1]).reshape(1,-1)
    print(feature_file)

    # new_df = empty_df()
    # new_df.loc[len(new_df)] = feature_file

    # # Saving the DataFrame to Excel
    # folder_path = os.path.dirname(file_path)
    # excel_name = os.path.join(folder_path, 'fitur.xlsx')
    # new_df.to_excel(excel_name, index=False)

    # # Convert the DataFrame to JSON
    # json_data = new_df.to_json(orient='records')

    # print(json_data)

    # Load the model
    # Loop through files in the directory
    predictions_dict = {}
    for filename in os.listdir(model_path):
        
        # Check if the file is a model file (adjust the condition as needed)
        if filename.endswith('.joblib'):
            # Load the model
            each_model_path = os.path.join(model_path, filename)
            print('model_1 path: ',model_path)
            loaded_model = load(each_model_path)
            
            # Use the loaded model for predictions or other purposes
            predictions = loaded_model.predict(feature_file)
            print(f"Predictions using {filename}: {predictions}")

            predictions_dict[filename] = predictions.tolist()

    return jsonify(predictions_dict), 200
    
# def feature_extraction()

import json

@app.route('/api/fetch-fitur', methods=['GET'])
def fetch():
    file_path = request.args.get('file_name')

    # print('file_path :', file_path)

    if file_path:
        return send_file(file_path, as_attachment=True)
    else:
        return 'File not found', 404
    
@app.route('/api/train-model', methods=['GET'])
def train_model():
    # try:
        print('\nTrain Model......')
        file_path = request.args.get('file_name')
        public_path = request.args.get('public_path')

        # Membagi string berdasarkan karakter "\"
        parts = file_path.split('\\')

        # Mengambil bagian yang diinginkan (di sini: indeks ke-6)
        model_folder = parts[6]
        print('file_path :', file_path)
        print('public_path :', public_path)
        model_save_path = public_path +'models\\'+model_folder
        print('\nmodel_path :', model_save_path)


        df = pd.read_excel(file_path)
        # cr_filename = nama file classification reports seluruh model
        accuracy_data, classification_reports = train_and_save_models(df, label='Label', model_save_path=model_save_path)

        response_data = {'success': True, 'accuracy': accuracy_data, 'model_path':model_save_path, 'classification_reports': classification_reports}
        return jsonify(response_data), 200
    # except Exception as e:
    #     print("Error:", str(e))
    #     return {'error': str(e)}, 500



if __name__ == '__main__':
    app.run(debug=True)  # Jalankan Flask di mode debug, sesuaikan dengan kebutuhan Anda
