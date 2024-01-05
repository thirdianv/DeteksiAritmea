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
    
def feature_extraction(data, label):
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

def feature(path):
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
    new_df.to_excel(name, index=False)
    return name


@app.route('/api/model', methods=['POST', 'GET'])
def model():
    if 'file_name' not in request.json:
        return jsonify({'error': 'Nama file tidak disediakan'}), 400

    file_name = request.json['file_name']
    folder_path = 'F:\\vicky\\example-app\\storage\\app\\public'  # Ganti dengan path folder Anda
    new_folder = file_check(file_name, folder_path)

    folder_name = os.path.splitext(os.path.basename(file_name))[0]  # Ambil nama file tanpa ekstensi
    destination_folder = os.path.join(folder_path, folder_name)
   
    # feature extraction
    feature_file = feature(destination_folder)

    feature_dict = {
        'feature_name': feature_file,
    }

    return jsonify(feature_dict)
    
# def feature_extraction():




if __name__ == '__main__':
    app.run(debug=True)  # Jalankan Flask di mode debug, sesuaikan dengan kebutuhan Anda
