import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/check-file', methods=['POST'])
def check_file():
    if 'file_name' not in request.json:
        return jsonify({'error': 'Nama file tidak disediakan'}), 400

    file_name = request.json['file_name']
    folder_path = 'F:\\vicky\\example-app\\storage\\app\\public'  # Ganti dengan path folder Anda

    if os.path.exists(os.path.join(folder_path, file_name)):
        return jsonify({'file_exists': True, 'message': f'File "{file_name}" ditemukan.'}), 200
    else:
        return jsonify({'file_exists': False, 'message': f'File "{file_name}" tidak ditemukan.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
