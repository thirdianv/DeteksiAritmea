<?php

namespace App\Http\Controllers;

use GuzzleHttp\Client;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Response;

class test extends Controller
{
    public function getPlot()
    {
        $client = new Client();
        $response = $client->get('http://127.0.0.1:5000/api/plot');
        
        // Ensure the response was successful
        if ($response->getStatusCode() === 200) {
            // Get the content type from the response headers
            $contentType = $response->getHeader('Content-Type')[0];

            // Set the appropriate content type for the Laravel response
            return Response::make($response->getBody(), 200, [
                'Content-Type' => $contentType,
                'Content-Disposition' => 'inline; filename="plot.png"', // Adjust as needed
            ]);
        } else {
            // Handle the case where the Python API did not return a 200 status
            return response()->json(['error' => 'Invalid response from Python API'], $response->getStatusCode());
        }
    }
}
