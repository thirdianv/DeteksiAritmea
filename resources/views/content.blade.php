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
        <button>Download File</button>
    </a>

    <form action="{{ route('load-model') }}" method="post">
        @csrf
        <input type="hidden" name="file_name" value="{{ $file_name }}">
        <button type="submit">Use File</button>
    </form>

</body>
</html>
