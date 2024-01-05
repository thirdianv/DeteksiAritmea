<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class ExcelController extends Controller
{
    public function showUploadForm()
    {
        return view('upload-model');
    }

    public function uploadExcel(Request $request)
    {
        $request->validate([
            'excelFile' => 'required|mimes:xlsx,xls|max:10240', // Max file size: 10 MB
        ]);

        $file = $request->file('excelFile');

        // Sanitize the filename to remove null bytes
        $sanitizedFilename = str_replace("\0", "", $file->getClientOriginalName());

        // Get the file content as a string
        $base64FileContent  = base64_encode(file_get_contents($file->getRealPath()));

        // Check if $fileContent is not false before using it
        if ($base64FileContent !== false) {
            
            $fileData = [
                'file' => $base64FileContent,
                'filename' => $sanitizedFilename,
            ];

            $response = Http::withHeaders(['Content-Type' => 'application/json'])
                            ->post('http://127.0.0.1:5000/train-model', $fileData);


            // Check if the request to the Flask API was successful
            if ($response->successful()) {
                // Handle success
                $responseData = $response->json();  
                // dd($responseData);
                $success = $responseData['success'];
                $accuracyData = $responseData['accuracy'];
                return view('trained-view', ['success' => $success, 'accuracyData' => $accuracyData]);

            } else {
                // Handle failure
                return redirect()->route('upload-model.form')->with('error', 'Failed to train model. Please try again.');
            }
        } else {
            // Handle the case where file_get_contents fails
            return redirect()->route('upload-model.form')->with('error', 'Failed to read file content.');
        }
    }
}
