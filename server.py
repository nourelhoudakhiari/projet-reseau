import socket
import threading
import json
from game import TicTacToe

class TicTacToeServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        
        self.games = {}
        self.players = {}
        self.player_count = 0
        
        print(f"Serveur démarré sur {host}:{port}")
    
    def broadcast_game_state(self, game_id):
        game = self.games[game_id]
        players = self.players[game_id]
        
        state = game.get_state()
        state_json = json.dumps({
            'board': state['board'].tolist(),
            'current_player': state['current_player'],
            'game_over': state['game_over'],
            'winner': state['winner'],
            'winning_line': state['winning_line']
        })
        
        for player in players.values():
            try:
                player.send(state_json.encode())
            except:
                pass
    
    def handle_client(self, conn, addr):
        print(f"Nouvelle connexion de {addr}")
        
        # Assigner un ID de joueur et une partie
        self.player_count += 1
        player_id = self.player_count
        game_id = (player_count + 1) // 2
        
        if game_id not in self.games:
            self.games[game_id] = TicTacToe()
            self.players[game_id] = {}
        
        # Envoyer l'ID du joueur
        conn.send(str(player_id % 2 + 1).encode())  # 1 ou 2
        
        self.players[game_id][player_id] = conn
        print(f"Joueur {player_id} ajouté à la partie {game_id}")
        
        try:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                
                if data == "GET_STATE":
                    self.broadcast_game_state(game_id)
                elif data.startswith("MOVE"):
                    _, row, col = data.split()
                    game = self.games[game_id]
                    
                    if game.current_player == (player_id % 2 + 1):
                        if game.make_move(int(row), int(col)):
                            self.broadcast_game_state(game_id)
                        else:
                            conn.send("INVALID_MOVE".encode())
                    else:
                        conn.send("NOT_YOUR_TURN".encode())
        
        except Exception as e:
            print(f"Erreur avec le client {addr}: {e}")
        finally:
            print(f"Connexion fermée avec {addr}")
            conn.close()
            if game_id in self.players and player_id in self.players[game_id]:
                del self.players[game_id][player_id]
    
    def start(self):
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    server = TicTacToeServer()
    server.start()