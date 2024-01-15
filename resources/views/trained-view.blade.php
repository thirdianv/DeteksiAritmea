<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Upload and Predict</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        .container {
            max-width: 600px;
            margin: auto;
        }
        .response-box {
            background-color: #f8f9fa;
            padding: 20px;
            border: 1px solid #d6d8db;
            border-radius: 5px;
            margin-top: 20px;
        }
        .alert-box {
            margin-top: 20px;
        }
        .toggle-button {
            margin-top: 20px;
        }
        .form-group{
            margin: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        @if(session('success'))
            <div class="alert alert-success">
                {{ session('success') }}
            </div>
        @endif

        @if(session('error'))
            <div class="alert alert-danger">
                {{ session('error') }}
            </div>
        @endif

        @if(isset($success) && $success)
            <div class="response-box">
                <div class="alert alert-success">
                    File uploaded and model trained successfully!
                </div>
                <h2 style="font-size: 20px; font-weight: bold; margin-bottom: 10px;">Results: Accuracy and Classification Report</h2>
                <button id="toggleAccuracyButton" class="btn btn-primary toggle-button">Show Results</button>
                <div id="accuracyDetails" style="display: none; padding: 20px; border: 1px solid #ccc; margin-top: 20px;">
                    @if(isset($accuracyData) && isset($classification_reports))
                        <p style="font-weight: bold;">KNN Accuracy: {{ number_format($accuracyData['knn_accuracy']*100, 2) }} %</p>
                        <p style="font-weight: bold;">SVC Accuracy: {{ number_format($accuracyData['svc_accuracy']*100, 2) }} %</p>
                        <p style="font-weight: bold;">Random Forest Accuracy: {{ number_format($accuracyData['rf_accuracy']*100, 2) }} %</p>
                
                        <div style="margin-top: 20px;">
                            <h2 style="font-weight: bold; margin-bottom: 10px; font-size: 20px;">KNN Classification Report</h2>
                            <pre>{{ $classification_reports['knn_classification_report'] }}</pre>
                        </div>
                
                        <div style="margin-top: 20px;">
                            <h2 style="font-weight: bold; margin-bottom: 10px; font-size: 20px;">SVC Classification Report</h2>
                            <pre>{{ $classification_reports['svc_classification_report'] }}</pre>
                        </div>
                
                        <div style="margin-top: 20px;">
                            <h2 style="font-weight: bold; margin-bottom: 10px; font-size: 20px;">Random Forest Classification Report</h2>
                            <pre>{{ $classification_reports['rf_classification_report'] }}</pre>
                        </div>
                    @endif
                </div>
                
                <h2 style="font-size: 20px; font-weight: bold; margin-bottom: 10px; margin-top: 20px;">Predict</h2>                
                <form id="uploadForm" action="{{ route('predict-data') }}" method="POST" enctype="multipart/form-data">
                    @csrf
                    <div class="form-group">
                        <label for="xlsxFile">Upload File:</label>
                        <input type="file" class="form-control-file" id="xlsxFile" name="xlsxFile">
                        <small class="form-text text-muted">Accepted file types: .xlsx, .csv, .xls</small>
                    </div>  
                    <input type="hidden" name="modelPath" value="{{ $modelPath }}">
                    <button type="button" id="uploadBtn" class="btn btn-primary">Upload</button>
                </form>                
                <div id="responseContainer" class="response-box">
                </div>
            </div>
        @else
            <div class="alert-box">
                <div class="alert alert-danger">
                    Failed to train the model. Please try again.
                </div>
            </div>
        @endif
    </div>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script>
        $(document).ready(function(){
            $('#uploadBtn').click(function(){
                var formData = new FormData($('#uploadForm')[0]);
    
                $.ajax({
                    url: "{{ route('predict-data') }}",
                    type: 'POST',
                    data: formData,
                    processData: false,
                    contentType: false,
                    dataType: 'json',
                    success: function(response){
                        console.log(response); // Log the entire JSON response
    
                        var htmlContent = '<h4 style=\'margin-bottom:20px\'>Hasil Prediksi :</h4>';
    
                        for (var key in response) {
                            if (response.hasOwnProperty(key)) {
                                var cleanKey = key.replace('.joblib', '');
                                var modifiedValues = response[key].map(function(value) {
                                    return value === 'A' ? 'Abnormal' : value === 'N' ? 'Normal' : value;
                                });
    
                                htmlContent += '<p><strong>Prediksi ' + cleanKey + ':</strong> ' + modifiedValues.join(', ') + '</p>';
                            }
                        }
    
                        $('#responseContainer').html(htmlContent);
                    },
                    error: function(xhr, status, error){
                        console.error(xhr, status, error);
                    }
                });
            });
    
            $('#toggleAccuracyButton').click(function() {
                $('#accuracyDetails').toggle();
            });
        });
    </script>
    
</body>
</html>
