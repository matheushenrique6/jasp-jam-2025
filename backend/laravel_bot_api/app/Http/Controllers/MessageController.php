<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Message;
use Illuminate\Support\Facades\Http;

class MessageController extends Controller
{
        public function index(Request $request)
    {
        $chat_id = $request->query('chat_id');
        return Message::where('chat_id', $chat_id)->latest()->take(50)->get();
    }

     public function store(Request $request)
    {
        $request->validate([
            'chat_id' => 'required',
            'text' => 'required|string',
            'direction' => 'required|in:incoming,outgoing',
        ]);

        return Message::create($request->all());
    }

     public function sendToBot(Request $request)
    {
        $request->validate([
            'chat_id' => 'required',
            'text' => 'required|string',
        ]);

        // Envia para o bot Python
        Http::post(env('BOT_PYTHON_URL').'/send', [
            'chat_id' => $request->chat_id,
            'text' => $request->text,
        ]);

        // Salva mensagem como "outgoing"
        return Message::create([
            'chat_id' => $request->chat_id,
            'text' => $request->text,
            'direction' => 'outgoing',
        ]);
    }
}
