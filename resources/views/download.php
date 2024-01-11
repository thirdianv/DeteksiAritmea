<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Fetch the file name from the POST request
    $file_name = $_POST['file_name']; // Change this according to your form's input name

    // Ensure the file exists before proceeding
    if (file_exists($file_name)) {
        // Set headers for file download
        header('Content-Description: File Transfer');
        header('Content-Type: application/octet-stream');
        header('Content-Disposition: attachment; filename="' . basename($file_name) . '"');
        header('Expires: 0');
        header('Cache-Control: must-revalidate');
        header('Pragma: public');
        header('Content-Length: ' . filesize($file_name));
        readfile($file_name); // Output the file
        exit;
    } else {
        echo 'File not found.';
    }
}
?>
