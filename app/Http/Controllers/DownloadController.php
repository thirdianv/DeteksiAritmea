<?php

namespace App\Http\Controllers;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\View;
use Illuminate\Http\Request;

class DownloadController extends Controller
{
    public function downloadFile(Request $request)
    {
        $file_name = $request->input('data');
        // dd($fileName);
        // $file_name = Storage::url($fileName);
        return view('/content', compact('file_name'));
    }
}
