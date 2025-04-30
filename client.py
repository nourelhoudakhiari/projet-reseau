import pygame
import sys
from pygame.locals import *

class GameMenu:
    def __init__(self):
        pygame.init()
        self.width, self.height = 600, 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tic Tac Toe - Menu")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 32)
        self.selected_mode = None
        
        self.options = [
            {"text": "1. Humain vs Humain (Local)", "rect": None, "key": K_1, "mode": "local_pvp"},
            {"text": "2. Humain vs IA", "rect": None, "key": K_2, "mode": "vs_ai"},
            {"text": "3. Jouer en ligne", "rect": None, "key": K_3, "mode": "online"},
            {"text": "4. Quitter", "rect": None, "key": K_4, "mode": "quit"}
        ]
        
        self.colors = {
            "background": (240, 240, 240),
            "text": (0, 0, 0),
            "hover": (100, 150, 255)
        }
        
    def draw_menu(self):
        self.screen.fill(self.colors["background"])
        title = self.font.render("Choisissez un mode de jeu", True, self.colors["text"])
        self.screen.blit(title, (self.width//2 - title.get_width()//2, 50))
        
        for i, option in enumerate(self.options):
            text_color = self.colors["hover"] if option["rect"] and option["rect"].collidepoint(pygame.mouse.get_pos()) else self.colors["text"]
            text = self.font.render(option["text"], True, text_color)
            
            text_rect = text.get_rect(center=(self.width//2, 150 + i*70))
            self.options[i]["rect"] = text_rect
            
            self.screen.blit(text, text_rect)
            
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                
                if event.type == KEYDOWN:
                    for option in self.options:
                        if event.key == option["key"]:
                            self.selected_mode = option["mode"]
                            running = False
                
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    for option in self.options:
                        if option["rect"] and option["rect"].collidepoint(mouse_pos):
                            self.selected_mode = option["mode"]
                            running = False
            
            self.draw_menu()
            self.clock.tick(60)
        
        pygame.quit()
        return self.selected_mode

class TicTacToeGUI:
    def __init__(self, is_ai_game=False):
        pygame.init()
        self.width, self.height = 600, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tic Tac Toe")
        
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.is_ai_game = is_ai_game
        self.ai_player = 'O' if is_ai_game else None
        
        self.font = pygame.font.SysFont('Arial', 120)
        self.small_font = pygame.font.SysFont('Arial', 40)
        
        self.colors = {
            "background": (255, 255, 255),
            "lines": (0, 0, 0),
            "X": (255, 0, 0),
            "O": (0, 0, 255),
            "text": (0, 0, 0)
        }
    
    def draw_board(self):
        self.screen.fill(self.colors["background"])
        
        # Dessiner les lignes du plateau
        pygame.draw.line(self.screen, self.colors["lines"], (self.width//3, 0), (self.width//3, self.height), 4)
        pygame.draw.line(self.screen, self.colors["lines"], (2*self.width//3, 0), (2*self.width//3, self.height), 4)
        pygame.draw.line(self.screen, self.colors["lines"], (0, self.height//3), (self.width, self.height//3), 4)
        pygame.draw.line(self.screen, self.colors["lines"], (0, 2*self.height//3), (self.width, 2*self.height//3), 4)
        
        # Dessiner les X et O
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 'X':
                    x = col * self.width//3 + self.width//6
                    y = row * self.height//3 + self.height//6
                    text = self.font.render('X', True, self.colors["X"])
                    self.screen.blit(text, (x - text.get_width()//2, y - text.get_height()//2))
                elif self.board[row][col] == 'O':
                    x = col * self.width//3 + self.width//6
                    y = row * self.height//3 + self.height//6
                    text = self.font.render('O', True, self.colors["O"])
                    self.screen.blit(text, (x - text.get_width()//2, y - text.get_height()//2))
        
        # Afficher le joueur actuel ou le gagnant
        status_rect = pygame.Rect(0, self.height - 50, self.width, 50)
        pygame.draw.rect(self.screen, self.colors["background"], status_rect)
        
        if self.game_over:
            if self.winner:
                status_text = f"Le gagnant est {self.winner} !"
            else:
                status_text = "Match nul !"
        else:
            status_text = f"Tour du joueur {self.current_player}"
        
        text = self.small_font.render(status_text, True, self.colors["text"])
        self.screen.blit(text, (self.width//2 - text.get_width()//2, self.height - 45))
        
        pygame.display.flip()
    
    def check_winner(self):
        # Vérifier les lignes
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != '':
                return self.board[row][0]
        
        # Vérifier les colonnes
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                return self.board[0][col]
        
        # Vérifier les diagonales
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]
        
        # Vérifier si le plateau est plein (match nul)
        if all(self.board[row][col] != '' for row in range(3) for col in range(3)):
            return 'tie'
        
        return None
    
    def make_ai_move(self):
        # IA simple qui joue au hasard
        import random
        empty_cells = [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == '']
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row][col] = self.ai_player
            self.current_player = 'X'
    
    def handle_click(self, pos):
        if self.game_over or (self.is_ai_game and self.current_player == self.ai_player):
            return
        
        col = pos[0] // (self.width // 3)
        row = pos[1] // (self.height // 3)
        
        if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == '':
            self.board[row][col] = self.current_player
            
            winner = self.check_winner()
            if winner:
                self.game_over = True
                self.winner = winner if winner != 'tie' else None
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                
                if self.is_ai_game and self.current_player == self.ai_player and not self.game_over:
                    self.make_ai_move()
                    winner = self.check_winner()
                    if winner:
                        self.game_over = True
                        self.winner = winner if winner != 'tie' else None
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)
                elif event.type == KEYDOWN and event.key == K_r and self.game_over:
                    # Réinitialiser le jeu si R est pressé
                    self.__init__(self.is_ai_game)
            
            self.draw_board()
            pygame.time.Clock().tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    menu = GameMenu()
    mode = menu.run()
    
    if mode == "quit":
        sys.exit()
    
    print(f"Mode sélectionné : {mode}")
    
    if mode == "local_pvp":
        game = TicTacToeGUI(is_ai_game=False)
        game.run()
    elif mode == "vs_ai":
        game = TicTacToeGUI(is_ai_game=True)
        game.run()
    elif mode == "online":
        print("Mode en ligne - À implémenter")
        # Ici vous pourriez ajouter le code pour le mode en ligne
        
