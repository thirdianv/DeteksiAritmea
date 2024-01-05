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
import os

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
    
    accuracy_data = {
        'knn_accuracy': knn_accuracy,
        'svc_accuracy': svc_accuracy,
        'rf_accuracy': rf_accuracy
    }
    # Save the models
    os.makedirs(model_save_path, exist_ok=True)
    joblib.dump(knn_model, f"{model_save_path}/knn_model.joblib")
    joblib.dump(svc_model, f"{model_save_path}/svc_model.joblib")
    joblib.dump(rf_model, f"{model_save_path}/rf_model.joblib")

    return accuracy_data