<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Show Images</title>
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
            max-width: 2000px;
            margin: 0 auto;
        }

        .image-column {
            flex: 0 0 calc(33.33% - 20px);
            margin: 10px;
        }

        .image-container img {
            width: 600px; /* Adjusted to make images larger */
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease-in-out;
        }

        .image-container img:hover {
            transform: scale(1.1);
        }

        .title-image {
            max-width: 800px;
            margin: 20px auto;
        }

        .title-image img {
            width: 100%;
            max-width: 800px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body>
    <h1>Image Gallery</h1>

    <div class="image-container">
        @foreach($images as $image)
            <div class="image-column">
                <img src="{{ asset('storage/'.$image) }}" alt="{{ asset('storage/'.$image) }}">
            </div>
        @endforeach
    </div>
</body>
</html>
