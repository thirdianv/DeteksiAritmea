<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plot Images</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            text-align: center;
        }

        h1 {
            color: #333;
            margin-top: 20px;
            margin-bottom: 30px; 
        }
        .image-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            max-width: 1200px;
            margin: 20px auto;
        }

        .image-column {
            flex: 0 0 calc(33.33% - 20px);
            margin: 10px;
            text-align: center;
        }

        .image-container img {
            width: 100%;
            max-width: 1200px; /* Adjust the max-width based on your preference */
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease-in-out;
            cursor: pointer;
        }

        .image-container img:hover {
            transform: scale(1.1);
        }

        .explanation-container {
            max-width: 1200px;
            margin: 20px auto;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
        }

        .explanation-column {
            flex: 1;
            margin: 10px;
            text-align: left;
            max-width: 400px;
            background-color: #fff;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease-in-out;
        }

        .explanation-column:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }

        .explanation-column h2 {
            color: #000000;
            margin-bottom: 10px;
        }

        .explanation-column p {
            color: #444;
            line-height: 1.6;
        }

        #previewModal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.7);
            justify-content: center;
            align-items: center;
        }

        #modalContent {
            background-color: #fff;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }

        #modalContent img {
            width: 100%;
            max-width: 3200px; /* Adjust the max-width based on your preference */
            border-radius: 8px;
        }

        #closeModal {
            position: absolute;
            top: 10px;
            right: 10px;
            cursor: pointer;
            color: #fff;
            font-size: 20px;
        }
    </style>
</head>
<body>
    <h1>Plot Images</h1>

  
    <div class="image-container">
        @foreach($images as $image)
            <div class="image-column">
                <img src="{{ asset('storage/'.$image) }}" alt="{{ asset($image) }}" onclick="openPreview('{{ asset('storage/'.$image) }}')">
            </div>
        @endforeach
    </div>

    <div class="explanation-container">
        <div class="explanation-column">
            <h2>Frequency Domain</h2>
            <p>
                The representation of a signal in the frequency domain reveals the frequency components that make up the signal. Complex signals can be decomposed into various frequency components. This representation is useful for understanding the frequency spectrum of a signal, i.e., the distribution of signal energy across different frequencies.
            </p>
        </div>
        <div class="explanation-column">
            <h2>Time Domain</h2>
            <p>
                In signal processing, the time domain refers to the representation of signals in the time or temporal dimension. It provides insights into how a signal varies over time and is essential for understanding the behavior of signals in practical applications.
            </p>
        </div>
    </div>

    <!-- Preview Modal -->
    <div id="previewModal">
        <div id="modalContent">
            <span id="closeModal" onclick="closePreview()">×</span>
            <img id="previewImage" src="" alt="Preview Image">
        </div>
    </div>
    <script>
        // JavaScript for opening preview modal
        function openPreview(imageUrl) {
            document.getElementById('previewImage').src = imageUrl;
            document.getElementById('previewModal').style.display = 'flex';
    
            // Adding event listener to close modal if clicked outside the modal
            window.addEventListener('click', outsideClick);
        }
    
        // JavaScript for closing preview modal
        function closePreview() {
            document.getElementById('previewModal').style.display = 'none';
    
            // Removing event listener after closing modal
            window.removeEventListener('click', outsideClick);
        }
    
        // Function to close modal if clicked outside the modal
        function outsideClick(e) {
            var modal = document.getElementById('modalContent');
            if (e.target === modal || modal.contains(e.target)) {
                closePreview();
            }
        }
    </script>
</body>
</html>
