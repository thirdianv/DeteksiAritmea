<!DOCTYPE html>
<html>
<head>
    <title>Download Page</title>
</head>
<body>
    <h1>Download Your File</h1>
    <p>Click the link below to download the file:</p>
    <p>{{ $file_name }}</p>
    <a href="{{ $file_name }}" download>
        <button href={{$file_name}}>Download File</button>
    </a>

</body>
</html>
