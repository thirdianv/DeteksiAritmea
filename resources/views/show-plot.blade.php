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
            max-width: 400px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease-in-out;
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
            max-width: 400px; /* Adjust the max-width based on your preference */
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
    </style>
</head>
<body>
    <h1>Plot Images</h1>

    <div class="image-container">
        @foreach($images as $image)
            <div class="image-column">
                <img src="{{ asset('storage/'.$image) }}" alt="{{ asset($image) }}">
            </div>
        @endforeach
    </div>

    <div class="explanation-container">
        <div class="explanation-column">
            <h2>DFT (Discrete Fourier Transform)</h2>
            <p>
                The Discrete Fourier Transform (DFT) is a mathematical technique that transforms a signal from its original domain (usually time or space) to the frequency domain. It is often used in signal processing and analysis to understand the frequency components present in a signal.
            </p>
        </div>

        <div class="explanation-column">
            <h2>Raw Signal</h2>
            <p>
                The raw signal represents the original data without any processing or transformation. It is the input data that is typically analyzed or processed to extract meaningful information.
            </p>
        </div>

        <div class="explanation-column">
            <h2>Time Domain</h2>
            <p>
                In signal processing, the time domain refers to the representation of signals in the time or temporal dimension. It provides insights into how a signal varies over time and is essential for understanding the behavior of signals in practical applications.
            </p>
        </div>
    </div>
</body>
</html>
