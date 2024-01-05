<!DOCTYPE html>
<html>
<head>
    <title>Upload File Zip</title>
</head>
<body>
    <h2>Upload File Zip</h2>
    <form method="POST" action="/upload" enctype="multipart/form-data">
        @csrf
        <input type="file" name="zip_file">
        <button type="submit">Unggah</button>
    </form>
</body>
</html>
