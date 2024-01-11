import pandas as pd
import pyhrv.frequency_domain as fd
import pyhrv.time_domain as td
import biosppy
import numpy as np
import os
import seaborn as sns
from tqdm import tqdm
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import RepeatedStratifiedKFold
import joblib


def upload_data(path):
    df = pd.read_excel(path)
    t = df[df.columns[0]]
    s1 = df[df.columns[1]]
    df_columns = df.columns
    return df, df_columns

def split_dataframe(result, chunk_size, output_directory='datas', output_prefix='normal'):
    os.makedirs(output_directory, exist_ok=True)
    chunks = list()
    num_chunks = len(result) // chunk_size
    for i in range(num_chunks):
        chunk = result[i * chunk_size:(i + 1) * chunk_size]
        chunks.append(chunk)
        output_filename = os.path.join(output_directory, f"{output_prefix}_{i}.xlsx")

        # Save the chunk to an Excel file
        chunk.to_excel(output_filename, index=False)

    return chunks

def feature_extraction(data, label ):
    numeric_data = pd.to_numeric(data, errors='coerce')
    numeric_data = numeric_data.dropna()
    # print(numeric_data)
    # mean rr
    mean_value = numeric_data.mean()

    # mean_value = sum(data)/len(data)
    # print(type(mean_value))
    # heart rate value
    hr_value = 60/mean_value
    # std
    std_hr = np.std(numeric_data)
    # cvr
    cvr_value = (std_hr/mean_value*100)
    # rmssd
    rmssd_value = np.sqrt(np.mean(np.square(np.diff(numeric_data))))
    # psd
    psd = fd.welch_psd(numeric_data, show =0)
    fd.plt.close()
    # peak psd
    peakPSD = psd['fft_peak']
    lfPeak_value = peakPSD[1]
    hfPeak_value = peakPSD[2]
    # norm psd
    normPSD = psd['fft_norm']
    lfNorm_value = normPSD[0]
    hfNorm_value = normPSD[1]
    # LF/HF
    lfhf_value = lfNorm_value/hfNorm_value
    # SDSD
    _sdsd = td.sdsd(numeric_data)
    _sdsd = _sdsd['sdsd']
    # NN50
    _nn50 = td.nn50(numeric_data)
    _nn50 = _nn50['nn50']

    return [mean_value, hr_value, std_hr, cvr_value, rmssd_value, _nn50, _sdsd, lfPeak_value, hfPeak_value, lfNorm_value, hfNorm_value, lfhf_value, label]
    # return [mean_value, hr_value, std_hr, rmssd_value, _nn50, _sdsd, lfPeak_value, hfPeak_value, lfNorm_value, hfNorm_value, lfhf_value, encoded_label]

def empty_df():
    # Dictionary with column names
    new_df = [
        'meanRR', 'HR', 'SDRR', 'CVR', 'RMSSD', 'NN50', 'SDSD', 'LF_Peak', 'HF_Peak', 'LF_Norm', 'HF_Norm', 'LF/HF', 'Label']
    # Convert the set of column names to a list
    columns_list = list(new_df)
    # Create an empty DataFrame with only headers
    new_df = pd.DataFrame(columns=columns_list)
    return new_df

def read_data(file_path):
    # df = pd.read_excel(file_path, header=[0, 1, 2])

    # data_columns=df.columns
    # df.drop(labels = data_columns[0], axis=1, inplace = True)
    # s1 = df[df.columns[1]]
    # return s1

    df = pd.read_excel(file_path, header=0)

    # Extract the first level of columns after dropping the specified level
    # data_columns=df.columns
  # df.drop(labels = data_columns[0], axis=1, inplace = True)
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


folder_path = './datas'

files = os.listdir(folder_path)

# create empty df
new_df = empty_df()
# print(new_df)

for file_name in files:
    if file_name.endswith('.xlsx'):
        # print(file_name)
        # print('\n')
        # read data
        data = read_data(folder_path +'/'+file_name)
        # label
        label = check_type(file_name)
        # print(type(label))
            # if label == 'Unknown':
            #     print(f"Skipping loop for '{file_name}' since label is Unknown")
            #     continue
        # feature extration
        fe = feature_extraction(data, label = label)
        # Append the new row to the DataFrame
        new_df.loc[len(new_df)] = fe
new_df.to_excel('ekstraksi_fitur.xlsx', index=False)

def plot_grid_histplot(df, df_columns, shape, figure_size):
    df_columns = np.array(df_columns).reshape(shape[0], shape[1])
    fig, axes = plt.subplots(shape[0],shape[1],figsize=figure_size)

    for i in range(df_columns.shape[0]):
        for j in range(df_columns.shape[1]):
            sns.histplot(data=df, x=df_columns[i,j], hue='Label', stat='density', bins=10, kde=True,
                palette=[sns.color_palette()[3], sns.color_palette()[0]],
                element='step', ax=axes[i, j])

    plt.show()

def pearson_corr(df):
    data_copy = df.replace(to_replace=['A','N'], value=[0,1], inplace = False)
    corr_df = data_copy.corr()
    print(corr_df)
    mask = np.zeros_like(data_copy.corr())
    mask[np.triu_indices_from(mask)] = True
    strong_relation_features = pd.Series(corr_df['Label']).nlargest(n=12).iloc[1:]
    feature = abs(strong_relation_features)
    # feature
    print(feature.sort_values(ascending=False))
    with sns.axes_style('darkgrid'):
        f, axes = plt.subplots(figsize=(20,10))
        sns.heatmap(data=data_copy.corr(), vmin=0, vmax=1, mask=mask, square=True, annot=True)
    plt.show()

def train_and_save_models(df, label, model_save_path):
    # Load the dataset
    # df = pd.read_csv(dataset_path)

    # Separate features (X) and target variable (y)
    X = df.drop('Label', axis=1)
    y = df['Label']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train K-Nearest Neighbors (KNN) model
    knn_model = KNeighborsClassifier()
    knn_model.fit(X_train, y_train)
    knn_predictions = knn_model.predict(X_test)
    knn_accuracy = accuracy_score(y_test, knn_predictions)
    
    # Train Support Vector Classifier (SVC) model
    svc_model = SVC()
    svc_model.fit(X_train, y_train)
    svc_predictions = svc_model.predict(X_test)
    svc_accuracy = accuracy_score(y_test, svc_predictions)

    # Train Random Forest model
    rf_model = RandomForestClassifier()
    rf_model.fit(X_train, y_train)
    rf_predictions = rf_model.predict(X_test)
    rf_accuracy = accuracy_score(y_test, rf_predictions)

    # Save the models
    joblib.dump(knn_model, f"{model_save_path}/knn_model.joblib")
    joblib.dump(svc_model, f"{model_save_path}/svc_model.joblib")
    joblib.dump(rf_model, f"{model_save_path}/rf_model.joblib")

    print(f"KNN Model Accuracy: {knn_accuracy}")
    print(f"SVC Model Accuracy: {svc_accuracy}")
    print(f"Random Forest Model Accuracy: {rf_accuracy}")


# result = upload_data('/Applications/XAMPP/xamppfiles/htdocs/TugasAkhir/DATA_N_30K.xlsx')#done
test_untuk_plot_distribusi = upload_data('/Applications/XAMPP/xamppfiles/htdocs/TugasAkhir/resampled_data.xlsx')
# print(test_untuk_plot_distribusi['df_columns'])
df = test_untuk_plot_distribusi[0]
df_columns = test_untuk_plot_distribusi[1]
label = df['Label']
# result_chunks = split_dataframe(result, chunk_size=100, output_directory='datas', output_prefix='normal')#done
# plot_grid_histplot(df, df_columns, shape=(6,2), figure_size=(14,22))#done
# pearson_corr(df)# done
# train_and_save_models(df, label, 'datas')#done


# Example usage: