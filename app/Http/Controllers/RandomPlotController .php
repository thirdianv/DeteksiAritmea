<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use GuzzleHttp\Client;

class RandomPlotController  extends Controller
{
    public function getPlot()
    {
        $client = new Client();
        $response = $client->get('http://127.0.0.1:5000/api/plot');
        $data = json_decode($response->getBody(), true);

        // Assuming the Python API returns the filename
        $plotFilename = $data['plot_filename'];

        // Display the plot
        return view('plot')->with('plotFilename', $plotFilename);
    }

    
}