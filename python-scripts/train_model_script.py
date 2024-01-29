from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import RepeatedStratifiedKFold
from imblearn.over_sampling import SMOTE
import pandas as pd
import numpy as np 
import json
import joblib
import os

def train_and_save_models(df, label, model_save_path):
    # Load the dataset
    # df = pd.read_csv(dataset_path)

    # Separate features (X) and target variable (y)
    X = df.drop('Label', axis=1)
    y = df['Label']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    testing_data = pd.concat([X_test, y_test], axis=1)
    class_counts = y_train.value_counts()

    # Check if any class has a difference greater than 25%
    is_imbalanced = (class_counts.max() - class_counts.min()) / class_counts.max() > 0.25

    if is_imbalanced:
        smote = SMOTE(random_state=42)
        X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)
    else:
        print("The dataset is balanced.")

    df_datatraining_smote = pd.concat([pd.DataFrame(X_train_smote), pd.Series(y_train_smote, name='Label')], axis=1)
    data_copy = df_datatraining_smote.replace(to_replace=['N','A'], value=[0,1],inplace=False)
    corr_df = data_copy.corr()
    strong_relation_features = pd.Series(corr_df['Label']).nlargest(n=8).iloc[1:]
    diagnosis = data_copy['Label']
    data_copy = data_copy[list(strong_relation_features.to_dict().keys())]
    data_copy['Label'] = diagnosis
    data_training = data_copy.sample(frac=1, random_state=42)
    X_train = data_training.drop(["Label"], axis = 1)
    y_train = data_training["Label"]
    y_train = y_train.replace(to_replace=[0,1], value=["N", "A"],inplace=False)
    # y_train = y_train.replace(to_replace=[0,1], value=["N", "A"],inplace=False)

    X_test = X_test.drop(["meanRR", "HR", "HF_Peak", "LF_Norm", "LF/HF"], axis = 1)
    following_feature = X_train.columns
    X_test = X_test.reindex(columns=following_feature)
    # y_test = y_test.replace(to_replace=['N','A'], value=[0,1],inplace=False)

    # Train K-Nearest Neighbors (KNN) model
    knn_model = KNeighborsClassifier(n_neighbors= 9, p= 1, weights= 'distance')
    knn_model.fit(X_train, y_train)
    knn_predictions = knn_model.predict(X_test)
    knn_accuracy = accuracy_score(y_test, knn_predictions)
    knn_classification_report = classification_report(y_test, knn_predictions)
    
    # Train Support Vector Classifier (SVC) model
    # svc_model = SVC(C= 10, gamma= 0.0001, kernel= 'rbf')
    svc_model = SVC()
    svc_model.fit(X_train, y_train)
    svc_predictions = svc_model.predict(X_test)
    svc_accuracy = accuracy_score(y_test, svc_predictions)
    svc_classification_report = classification_report(y_test, svc_predictions)

    # Train Random Forest model
    rf_model = RandomForestClassifier(max_depth=50, min_samples_leaf=1, min_samples_split=2, n_estimators=50)
    rf_model.fit(X_train, y_train)
    rf_predictions = rf_model.predict(X_test)
    rf_accuracy = accuracy_score(y_test, rf_predictions)
    rf_classification_report = classification_report(y_test, rf_predictions)

    classification_reports_data = {
        'knn_classification_report': knn_classification_report,
        'svc_classification_report': svc_classification_report,
        'rf_classification_report': rf_classification_report
    }
    os.makedirs(model_save_path, exist_ok=True)
    classification_reports_json = json.dumps(classification_reports_data, indent=4)

    json_filename = model_save_path +'/classification_report.json'
    # Writing to sample.json
    with open(json_filename, "w") as outfile:
        outfile.write(classification_reports_json)

    accuracy_data = {
        'knn_accuracy': knn_accuracy,
        'svc_accuracy': svc_accuracy,
        'rf_accuracy': rf_accuracy
    }

    combined_data = {
        'accuracy_data': accuracy_data,
        'classification_reports': classification_reports_data
    }

    # Save the models
    joblib.dump(knn_model, f"{model_save_path}/KNN.joblib")
    joblib.dump(svc_model, f"{model_save_path}/SVC.joblib")
    joblib.dump(rf_model, f"{model_save_path}/RF.joblib")

    print("model_save :", model_save_path)
    print("json_file :", json_filename)


    return accuracy_data, classification_reports_data
