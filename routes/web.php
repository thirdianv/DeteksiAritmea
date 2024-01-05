<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\RandomPlotController;
use App\Http\Controllers\FileUploadController;
use App\Http\Controllers\DownloadController;
use Psy\VersionUpdater\Downloader;
use App\Http\Controllers\ExcelController;

// use App\Http\Controllers\test;
/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

// Route::get('/api/plot', [App\Http\Controllers\RandomPlotController::class, 'getPlot']);
Route::get('/api/plot', [App\Http\Controllers\test::class, 'getPlot']);
Route::get('/api/extract-features', [App\Http\Controllers\test::class, 'extract']);
Route::get('/upload-form', [FileUploadController::class, 'showUploadForm']);
Route::post('/upload', [FileUploadController::class, 'upload']);
Route::post('/api/extract', [FileUploadController::class, 'extract']);
Route::get('/download-file/{data}', [DownloadController::class, 'downloadFile'])->name('download.file');
Route::get('/download-data', [DownloadController::class, 'downloadFile'])->name('DownloadController');


// Route::get('/api/plot', [App\Http\Controllers\test::class, 'asdasdasd']);

    
Route::group(['middleware' => ['web']], function () {
    Route::get('/upload-model', [ExcelController::class, 'showUploadform'])->name('upload-model.form');
    Route::post('/upload-model', [ExcelController::class, 'uploadExcel'])->name('upload-model');
});

// In routes/web.php

// Route::get('/trained-view', [ExcelController::class, 'uploadExcel'])->name('trained-view');
Route::get('/trained-view', function () {
    return view('trained-view');
})->name('trained-view');


// use Illuminate\Support\Facades\Route;

// Route::get('/show-classification-report', function () {
//     return view('show-classification-report');
// })->name('trained-view');;

    