from flask import Flask, send_file, jsonify, request
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend
import matplotlib.pyplot as plt
import io
import pandas as pd
import os 

app = Flask(__name__)

# df = pd.read_excel('C:\\xampp\\htdocs\\example-app\\DATA_N_30K.xlsx', header=[0,1])
# df = pd.read_excel('F:\\vicky\\example-app\\DATA_N_30K.xlsx', header=[0,1])


@app.route('/api/plot', methods=['GET'])
def generate_plot():

    df = pd.read_excel('F:\\vicky\\example-app\\normal_499.xlsx', header=[0,1])
    sample = df[df.columns[0]]
    signal = df[df.columns[1]]
    N = len(df.index)

    # RAW SIGNAL PLOTTING
    plt.plot(sample, signal)
    plt.xlabel('Sample')
    plt.ylabel('Amplitudo (mV)')
    plt.title("Raw Signal")
    plt.show()
    # ============================================================================================================
    # fs = 1/(sum(signal)/N)
    # ts = 1/fs

    # TIME DOMAIN PLOTTING
    # x = sample * ts
    # y = signal
    # # plt.figure(figsize=(20,6))
    # plt.plot(x,y)
    # plt.xlabel('Time (s)')
    # plt.xlim(0, 1000)
    # # plt.xticks=(np.arange(0,50))
    # plt.ylim(0.4, 1)
    # plt.ylabel('Amplitudo (mV)')
    # plt.title("Time Domain Signal")
    # plt.show()

    # Save the plot to a file-like object
    # img_buffer = io.BytesIO()
    # plt.savefig(img_buffer, format='png')
    # img_buffer.seek(0)

    # Clear the plot for the next request
    # plt.clf()

    # Return the image directly
    # return send_file(img_buffer, mimetype='image/png')

# @app.route('/splitting-data', methods=['GET', 'POST'])
# def split_dataframe():
#     content_type = request.headers.get('Content-Type')

#     if content_type and 'application/json' in content_type:
#         try:
#             data = request.json 
#             chunk_size = data.get('chunk_size', 300)
#             output_directory = data.get('output_directory', 'datas')
#             output_prefix = data.get('output_prefix', 'normal')
#             os.makedirs(output_directory, exist_ok=True)

#             chunks = list()
#             num_chunks = len(df) // chunk_size
#             for i in range(num_chunks):
#                 chunk = df[i * chunk_size:(i + 1) * chunk_size]
#                 chunks.append(chunk)
#                 output_filename = os.path.join(output_directory, f"{output_prefix}_{i}.xlsx")

#                 # Save the chunk to an Excel file
#                 chunk.to_excel(output_filename)

#             # Return the chunks as JSON
#             return jsonify({'chunks': chunks})

#         except Exception as e:
#             error_message = f"An error occurred: {str(e)}"
#             return jsonify({'error': error_message}), 500
#     else:
#         return jsonify({'error': 'Unsupported Content-Type'}), 415  # Unsupported Media Type

@app.route('/upload-form', methods=['GET', 'POST'])
def extract_features_from_spreadsheet():
    try:
        print("Attempting to read the Excel file...")
        # Read data from Excel file
        
        filename = 'F:\\vicky\\example-app\\normal_499.xlsx'

        df = pd.read_excel(filename)
        df.columns = df.columns.str.strip()
        print("Excel file read successfully!")

        column_names_to_check = ['sample', 'RR']

        # Assuming 'sample' and 'RR' columns are in the spreadsheet
        sample_column_name = 'sample'  # Replace with the actual column name in your spreadsheet
        RR_column_name = 'RR'  # Replace with the actual column name in your spreadsheet

        print("Checking column existence...")
        missing_columns = [col for col in column_names_to_check if col not in df.columns]

        if missing_columns:
            print(df.columns)
            print(f"Missing columns: {missing_columns}")
            return jsonify({'error': 'Data or label column(s) not found in the spreadsheet'}), 400


        print("Columns found, proceeding with feature extraction...")
        # Extract 'sample' and 'RR' columns from the DataFrame
        data = df[RR_column_name]
        label = check_type(filename)

        # Perform feature extraction similar to the previous code
        numeric_data = pd.to_numeric(data, errors='coerce').dropna()
        mean_value = numeric_data.mean()
        hr_value = 60 / mean_value
        std_hr = np.std(numeric_data)
        cvr_value = (std_hr / mean_value) * 100
        rmssd_value = np.sqrt(np.mean(np.square(np.diff(numeric_data))))

        # Additional calculations using scipy or other libraries as needed
        # ...

        result = {
            'mean_value': mean_value,
            'hr_value': hr_value,
            'std_hr': std_hr,
            'cvr_value': cvr_value,
            'rmssd_value': rmssd_value,
            # Add other values here
            'label': label # Convert label to a list for JSON serialization
        }

        print("Feature extraction completed, returning results...")
        return jsonify(result), 200

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
def check_type(file_name):
    # Split the file name using '_' as the separator
    parts = file_name.split('\\')

    # Extract the desired part before the underscore
    result = parts[-1]

    parts = result.split('_')
    result = parts[0]

    print(result)
    # Check if the result is 'normal' or 'abnormal'
    if result.lower() == 'normal':
        return 'N'
    elif result.lower() == 'abnormal':
        return 'A'
    else:
        return 'Unknown'

if __name__ == '__main__':
    app.run(debug=True)
