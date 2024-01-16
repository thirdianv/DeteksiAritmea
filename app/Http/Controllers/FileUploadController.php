<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use GuzzleHttp\Client;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\View;
use Illuminate\Support\Facades\File;



class FileUploadController extends Controller
{
    public function showUploadForm()
    {
        return view('upload-form');
    }

    public function upload(Request $request)
    {
        // make debug using console
        // Validasi bahwa file yang diunggah adalah file zip
        $request->validate([
            'zip_file' => 'required|file|mimes:zip,rar|max:10240', // Wajib ada, harus file ZIP/RAR, maksimal 10240KB (10MB)
        ]);
        
        
        // dd($request);
        if ($request->hasFile('zip_file')) {
            $file = $request->file('zip_file');
            $fileName = time() . '_' . $file->getClientOriginalName();

            $file->storeAs('public', $fileName); // Simpan file di storage public
            $path = storage_path('app\\public\\');
            // dd($path, $fileName);

            $data = [
                'file_name' => $fileName,
                'file_path' => $path,
            ];


            $url = 'http://127.0.0.1:5000/api/model'; // Sesuaikan dengan alamat API Flask Anda
            $client = new Client();
            // $response = $client->get($url, ['file_name' => $fileName]);
            
            $response = $client->post($url, [
                'json' =>$data
            ]);
            $statusCode = $response->getStatusCode();
            $responseData = json_decode($response->getBody(), true);

            if ($statusCode === 200){
                // echo 'File berhasil diunggah' . "\n";

                // $jsonStr = json_encode($response);

                // // Print the JSON string
                // echo $jsonStr;
                $file_name = $responseData['feature_name'];
                $files= dirname($file_name);
                
                // echo $file_name;
                // print($file_name);
                // dd($files);

                return redirect()->route('DownloadController', ['data' => $file_name, 'file' => file_get_contents($file_name), 'files'=>$files]);
                // return View::make('/content', compact('file_name'));
                // $path = $responseData['message'];
                // $files = scandir($path);
                
            }else{
                echo 'File gagal diunggah';
            }
        }
    }

    public function process_data(Request $request){

    }
}
