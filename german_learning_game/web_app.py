from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict

from .game_manager import GameManager

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active game sessions
game_sessions: Dict[str, GameManager] = {}


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    
    if session_id not in game_sessions:
        game_sessions[session_id] = GameManager()
    
    game = game_sessions[session_id]
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data["type"] == "start_game":
                await game.start_new_game(data["difficulty"])
                await websocket.send_json({"status": "game_started"})
            
            elif data["type"] == "user_input":
                await game.handle_user_input(data["text"])
                # Response will be handled through the event system
            
            elif data["type"] == "next_scene":
                await game.advance_scene()
                # Scene will be sent through the event system
    
    except Exception as e:
        print(f"Error in websocket connection: {e}")
    finally:
        if session_id in game_sessions:
            del game_sessions[session_id]


def run_server(port: int = 53685):
    """Run the FastAPI server."""
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        ws_ping_interval=None,
        ws_ping_timeout=None
    )