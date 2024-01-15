<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;


class PlotFileController extends Controller
{
    public function showPlot(Request $request)
    {
        $response = Http::get('http://127.0.0.1:5000/plot', [
            'file_name' => $request->input('filename'),
            'file_path_fitur' => $request->input('file_path_fitur')
        ]);

        // dd($request->input());
        
        if ($response->successful()) {
            $images = $response->json('images');
        
            return view('show-plot', compact('images'));
        } else {
            return response()->json(['error' => 'Failed to retrieve plot data'], $response->status());
        }
        
    }
}
