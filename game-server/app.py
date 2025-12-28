from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room, emit
from game_logic import CardGame

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory storage for rooms. 
# Replace with Redis for production use.
rooms = {} 

@socketio.on('join_game')
def handle_join(data):
    room_id = data.get('room')
    player_name = data.get('name', 'Anonymous')
    
    if room_id not in rooms:
        rooms[room_id] = CardGame()
    
    game = rooms[room_id]
    
    if len(game.players) >= 6:
        emit('error', {'message': 'Room is full (max 6)'})
        return

    if game.add_player(request.sid, player_name):
        join_room(room_id)
        print(f"Player {player_name} joined room {room_id}")
        
        # Notify everyone in the room
        emit('room_update', game.get_state(), to=room_id)
    else:
        emit('error', {'message': 'Could not join game.'})

@socketio.on('start_game')
def handle_start(data):
    room_id = data.get('room')
    game = rooms.get(room_id)
    
    if game and len(game.players) >= 2:
        game.deal_cards()
        # Send individual hands to each player privately
        for player in game.players:
            emit('deal_hand', {'hand': player['hand']}, to=player['id'])
        
        # Send general game state to everyone
        emit('room_update', game.get_state(), to=room_id)

@socketio.on('disconnect')
def handle_disconnect():
    for room_id, game in rooms.items():
        if any(p['id'] == request.sid for p in game.players):
            game.remove_player(request.sid)
            leave_room(room_id)
            emit('room_update', game.get_state(), to=room_id)
            break

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)