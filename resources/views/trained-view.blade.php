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
    <div class="alert-box centered-details">
        <div class="alert alert-success">
            File uploaded and model trained successfully!
        </div>
        <button id="toggleAccuracyButton" class="button-box">Toggle Accuracy</button>
        <div id="accuracyDetails" class="centered-details" style="display: none;">
            @if(isset($accuracyData))
                <p>KNN Accuracy: {{ $accuracyData['knn_accuracy'] }}</p>
                <p>SVC Accuracy: {{ $accuracyData['svc_accuracy'] }}</p>
                <p>Random Forest Accuracy: {{ $accuracyData['rf_accuracy'] }}</p>
                <!-- Add a link to the new view here -->
                {{-- <p>
                    <a href="{{ route('show-classification-report') }}">Show Classification Report</a>
                </p> --}}
                    
            @endif
        </div>
    </div>
@else
    <div class="alert-box">
        <div class="alert alert-danger centered-details">
            Failed to train the model. Please try again.
        </div>
    </div>
@endif

<style>
    .alert-box {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 1;
    }

    .centered-details {
        background-color: #f8f9fa;
        padding: 20px;
        border: 1px solid #d6d8db;
        border-radius: 5px;
        text-align: center;
    }

    .button-box {
        margin-top: 20px;
    }
</style>

<script>
    var accuracyDetails = document.getElementById('accuracyDetails');
    var toggleAccuracyButton = document.getElementById('toggleAccuracyButton');

    toggleAccuracyButton.addEventListener('click', function() {
        accuracyDetails.style.display = (accuracyDetails.style.display === 'none') ? 'block' : 'none';
    });
</script>
