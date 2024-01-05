import requests

url = 'http://127.0.0.1:5000/api/check-file'  # Ganti URL dengan alamat API Flask Anda
file_to_check = '1704390355_Downloads.rar'  # Ganti dengan nama file yang ingin Anda olah

# Payload JSON yang akan dikirim dalam permintaan POST
payload = {'file_name': file_to_check}

try:
    response = requests.post(url, json=payload)
    print(response)

    # Cek status code dari respons
    if response.status_code == 200:
        data = response.json()
        if data['file_exists']:
            print(f"File '{file_to_check}' ditemukan.")
        else:
            print(f"File '{file_to_check}' tidak ditemukan.")
    else:
        print(f"Gagal: {response.status_code}")
except requests.RequestException as e:
    print(f"Ada kesalahan dalam permintaan: {e}")