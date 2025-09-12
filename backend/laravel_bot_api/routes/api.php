<?php

use App\Http\Controllers\MessageController;

Route::get('/message', [MessageController::class, 'index']);
Route::post('/messages', [MessageController::class, 'store']);
Route::post('/send-message', [MessageController::class, 'sendToBot']);
